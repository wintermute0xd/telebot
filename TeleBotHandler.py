import requests
import datetime
import logging


class TeleBotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot' + token + '/'

    def get_updates(self, offset=None, timeout=30):
        logging.info('Started')
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        try:
            resp = requests.get(self.api_url + method, params)
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            logging.error('Can not connect to Telegram API')
            return None
        result_json = resp.json()['result']
        return result_json