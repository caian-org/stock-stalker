import requests

class SheetWebApp:
    def __init__(self, sheet_id, access_token):
        self.base_url = f'https://script.google.com/macros/s/{sheet_id}/exec'
        self.access_token = access_token

    def get_tickers(self):
        res = requests.get(self.base_url, params={'accessToken': self.access_token})
        if res.status_code != 200:
            raise Exception('(SheetWebApp) Request failed. Got: {}'.format(res.content))

        res = res.json()
        if res['status'] != 200:
            raise Exception('(SheetWebApp) Got status "{}"'.format(res['status']))

        return res['data']
