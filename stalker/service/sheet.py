# standard
import json

# 3rd-party
import requests


class SheetWebApp:
    def __init__(self, sheet_id, access_token):
        self.base_url = f'https://script.google.com/macros/s/{sheet_id}/exec'
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

    def _auth(self):
        return {'accessToken': self.access_token}

    def get_tickers(self):
        res = requests.get(self.base_url, params=self._auth())
        return self._data(res)

    def update(self, data):
        res = requests.post(self.base_url, params=self._auth(), json=data)
        return self._data(res)
