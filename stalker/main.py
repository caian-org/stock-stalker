import json

from service.sheet import SheetWebApp
from service.stock import StocksData
from lib.env import environment as env


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

    response = []
    for stocks in StocksData(codes).fetch():
        item = transposed.get(stocks.code)
        response.append(dict(item, value=round(stocks.value, 2), update=stocks.updated_at))

    print(json.dumps(response))


if __name__ == '__main__':
    handler(None, None)
