# modules
from stalker.lib.config import config

from stalker.service.sheet import SheetWebApp
from stalker.service.stock import StocksData
from stalker.service.telegram import TelegramBot


# pylint: disable=unused-argument
def handler(event, context):
    sheet = SheetWebApp(config.get('SCRIPT_ID'), config.get('SCRIPT_ACCESS_TOKEN'))
    telegram = TelegramBot(
        config.get('TELEGRAM_BOT_TOKEN'), config.get('TELEGRAM_DEST_USER')
    )

    codes = []
    transposed = {}

    for ticker in sheet.get_tickers():
        code = ticker['code']

        codes.append(code)
        transposed[code] = ticker

    tickers = []
    to_notify = {'buy': [], 'sell': []}

    for stocks in StocksData(codes).fetch():
        ticker = transposed.get(stocks.code)
        ticker = dict(ticker, value=round(stocks.value, 2), update=stocks.updated_at)

        if ticker['isBought']:
            if ticker['value'] >= ticker['expSell']:
                to_notify['sell'].append(ticker)
        else:
            if ticker['value'] <= ticker['expBuy']:
                to_notify['buy'].append(ticker)

        tickers.append(ticker)

    sheet.update(dict(tickers=tickers))

    if to_notify['buy']:
        telegram.notify_buy(to_notify['buy'])

    if to_notify['sell']:
        telegram.notify_sell(to_notify['sell'])
