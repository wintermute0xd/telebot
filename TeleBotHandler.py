import requests
import datetime
import logging

'''
Class for telegram bot.
Can get updates from Telegram API and make response in depends of chat text message.
'''


class TeleBotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot' + token + '/'

    # gets updates from telegram api by GET and returning update json object
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

    def request_handler(self, update):
        hello_text = ['hello', 'good day', 'good morning', 'good evening', 'привет', 'привіт', 'добрый день', 'доброго дня']

        now = datetime.datetime.now()
        cur_hour = now.hour
        in_text = update['message']['text']
        chat_name = update['message']['chat']['first_name']
        bot_response = 'I don\'t understand you'

        if in_text.lower() in hello_text:
            if 4 <= cur_hour <= 12:
                bot_response = 'Good morning'
            elif 12 < cur_hour <= 17:
                bot_response = 'Good day'
            elif 17 < cur_hour <= 22:
                bot_response = 'Good evening'
            elif 22 < cur_hour < 4:
                bot_response = 'Good night'

        return bot_response + ', ' + chat_name

    def send_message(self, chat_id, out_text):
        params = {'chat_id': chat_id, 'text': out_text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

