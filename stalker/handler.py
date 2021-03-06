# modules
from stalker.lib.config import config as cfg

from stalker.service.sheet import SheetWebApp
from stalker.service.stock import StocksData
from stalker.service.telegram import TelegramBot


# pylint: disable=unused-argument
def handler(event, context):
    sheet = SheetWebApp(
        cfg.get('SCRIPT_ID'), cfg.get('SCRIPT_ACCESS_TOKEN'), bool(cfg.get('IS_DEBUG'))
    )

    telegram = TelegramBot(cfg.get('TELEGRAM_BOT_TOKEN'), cfg.get('TELEGRAM_DEST_USER'))

    codes = []
    transposed = {}

    response = sheet.get_tickers()
    tickers = response['content']
    if not tickers:
        return

    for ticker in tickers:
        code = ticker['code']

        codes.append(code)
        transposed[code] = ticker

    tickers = []
    to_buy = []
    to_sell = []

    for stocks in StocksData(codes).fetch():
        ticker = transposed.get(stocks.code)
        ticker = dict(ticker, value=round(stocks.value, 2), update=stocks.updated_at)

        if ticker['isBought']:
            if ticker['value'] >= ticker['expSell']:
                to_sell.append(ticker)
        else:
            if ticker['value'] <= ticker['expBuy']:
                to_buy.append(ticker)

        tickers.append(ticker)

    sheet.update(dict(tickers=tickers))

    if to_buy or to_sell:
        telegram.notify_alert()

        if to_buy:
            telegram.notify_buy(to_buy)

        if to_sell:
            telegram.notify_sell(to_sell)
