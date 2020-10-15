# pylint: disable=anomalous-backslash-in-string

# 3rd-party
import requests


class TelegramBot:
    def __init__(self, token, user):
        self.base_url = f'https://api.telegram.org/bot{token}'
        self.user = user

    @property
    def _chart_up_emoji(self):
        return '\U0001F4C8'

    @property
    def _chart_down_emoji(self):
        return '\U0001F4C9'

    @staticmethod
    def _sanitize(message):
        return str(message).replace('.', '\.')

    def _send(self, message):
        res = requests.post(
            f'{self.base_url}/sendMessage',
            json={'parse_mode': 'MarkdownV2', 'chat_id': self.user, 'text': message},
        )

        if res.status_code != 200:
            raise Exception('(TelegramBot) Request failed. Got: {}'.format(res.content))

        return res.json()

    def notify_buy(self, tickers):
        message = self._chart_down_emoji + ' *TIME TO BUY*\!\n\n'

        for ticker in tickers:
            message = '{} \- `{}` \(exp `{}`, now `{}`\)\n'.format(
                message,
                self._sanitize(ticker['code']),
                self._sanitize(ticker['expBuy']),
                self._sanitize(ticker['value']),
            )

        return self._send(message)

    def notify_sell(self, tickers):
        message = self._chart_up_emoji + ' *TIME TO SELL*\!\n\n'

        for ticker in tickers:
            message = '{} \- `{}` \(exp `{}`, now `{}`\)\n'.format(
                message,
                self._sanitize(ticker['code']),
                self._sanitize(ticker['expSell']),
                self._sanitize(ticker['value']),
            )

        return self._send(message)
