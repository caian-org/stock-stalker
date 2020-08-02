import json

from stalker.service.sheet import SheetWebApp
from stalker.service.stock import StocksData
from stalker.lib.env import environment as env


def handler(event, context):
    sheet = SheetWebApp(
        env.get('SCRIPT_ID'),
        env.get('SCRIPT_ACCESS_TOKEN'))

    codes = []
    transposed = {}

    for ticker in sheet.get_tickers():
        code = ticker['code']

        codes.append(code)
        transposed[code] = ticker

    tickers = []
    to_notify = []

    for stocks in StocksData(codes).fetch():
        ticker = transposed.get(stocks.code)
        ticker = dict(ticker, value=round(stocks.value, 2), update=stocks.updated_at)

        if ticker['isBought']:
            if ticker['value'] >= ticker['expSell']:
                to_notify.append(ticker)
        else:
            if ticker['value'] <= ticker['expBuy']:
                to_notify.append(ticker)

        tickers.append(ticker)

    sheet.update(dict(tickers=tickers))
