# 3rd-party
import yfinance as yf

# modules
from .ticker import Ticker


# pylint: disable=too-few-public-methods
class StocksData:
    def __init__(self, tickers):
        self.tickers = tickers

    @staticmethod
    def _tail(data, key):
        return data.at[data.index[-1], key]

    def fetch(self):
        data_set = yf.download(
            tickers=' '.join(self.tickers),
            period='1d',
            interval='5m',
            group_by='ticker',
        )

        for ticker in self.tickers:
            data = data_set[ticker]

            close_value = data.at[data.index[-1], 'Close']
            updated_at = data.index[-1].strftime('%Y-%m-%d %H:%M:%S')

            yield Ticker(ticker, close_value, updated_at)
