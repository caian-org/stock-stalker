import yfinance as yf


class Ticker:
    def __init__(self, code, value, updated_at):
        self._code = code
        self._value = value
        self._updated_at = updated_at

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def updated_at(self):
        return self._updated_at


class StocksData:
    def __init__(self, tickers):
        self.tickers = tickers

    def _tail(self, data, key):
        return data.at[data.index[-1], key]

    def fetch(self):
        data_set = yf.download(
            tickers=' '.join(self.tickers),
            #tickers='GFSA3.SA HGTX3.SA TIET11.SA AMAR3.SA PFRM3.SA',
            period='1d',
            interval='5m',
            group_by='ticker')

        for ticker in self.tickers:
            data = data_set[ticker]

            close_value = data.at[data.index[-1], 'Close']
            updated_at = data.index[-1].strftime('%Y-%m-%d %H:%M:%S')

            yield Ticker(ticker, close_value, updated_at)
