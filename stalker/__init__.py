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

    response = []
    for stocks in StocksData(codes).fetch():
        item = transposed.get(stocks.code)
        response.append(dict(item, value=round(stocks.value, 2), update=stocks.updated_at))

    print(json.dumps(response))
