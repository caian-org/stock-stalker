# standard
import json

# 3rd-party
import requests


class SheetWebApp:
    def __init__(self, sheet_id, access_token, is_debug):
        self.base_url = f'https://script.google.com/macros/s/{sheet_id}/exec'

        self.is_debug = is_debug
        self.access_token = access_token

    @staticmethod
    def _data(res):
        if res.status_code != 200:
            raise ConnectionError(
                '(SheetWebApp) Request failed. Got: {}'.format(res.content)
            )

        res = res.json()
        if res['status'] != 200:
            raise ConnectionError(
                '(SheetWebApp) Got status {}; Response is: {}'.format(
                    res['status'], json.dumps(res['data'])
                )
            )

        return res.get('data')

    def _params(self):
        prms = {
            'accessToken': self.access_token,
        }

        if self.is_debug:
            prms['isDebug'] = '1'

        return prms

    def get_tickers(self):
        res = requests.get(self.base_url, params=self._params())
        return self._data(res)

    def update(self, data):
        res = requests.post(self.base_url, params=self._params(), json=data)
        return self._data(res)
