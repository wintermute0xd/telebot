import requests
import datetime
import logging
import json


'''
Class for telegram bot.
Can get updates from Telegram API and make response in depends of chat text message.
'''


class TeleBotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot' + token + '/'
        with open('bot_text.json', 'r', encoding='utf-8') as text_file:
            self.bot_text = json.load(text_file)

    # gets updates from telegram api via GET and returning update json object
    def get_updates(self, offset=None, timeout=60):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        try:
            resp = requests.get(self.api_url + method, params)
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            logging.error('Can not connect to Telegram API')
            return None
        result_json = resp.json()['result']
        return result_json

    def get_message_key(self, update):
        # check if message was edited
        if 'message' in update:
            self.message_key = 'message'
        else:
            self.message_key = 'edited_message'

        return self.message_key

    # makes dict with message type (text, photo, etc), send method and response msg itself
    def response_formatter(self, msg_type, resp):
        if msg_type == 'text':
            method = 'sendMessage'
        elif msg_type == 'photo':
            method = 'sendPhoto'
        else:
            method = 'sendMessage'
        bot_response = {'type': msg_type, 'resp': resp, 'method': method}
        return bot_response

    def is_command(self, update):
        if 'entities' in update[self.message_key] and update[self.message_key]['entities'][0]['type'] == 'bot_command':
            return True
        else:
            return False

    # requests random dog or random cat api and returns image url
    def get_dog(self, dog_api_url):
        contents = requests.get(dog_api_url).json()
        return contents['url']

    def get_cat(self, cat_api_url):
        contents = requests.get(cat_api_url).json()
        return contents[0]['url']

    def request_handler(self, update):

        hello_text = ['hello', 'good day', 'good morning', 'good evening', 'привет', 'привіт', 'добрый день', 'доброго дня']
        now = datetime.datetime.now()
        cur_hour = now.hour

        if self.is_command(update):
            return self.command_handler(update)

        in_text = update[self.message_key]['text']
        chat_name = update[self.message_key]['chat']['first_name']
        lang = update[self.message_key]['from']['language_code']
        response = 'I don\'t understand you'

        if in_text.lower() in hello_text:
            if 4 <= cur_hour <= 12:
                response = self.bot_text['hello_morning'][lang]
            elif 12 < cur_hour <= 17:
                response = self.bot_text['hello_day'][lang]
            elif 17 < cur_hour <= 22:
                response = self.bot_text['hello_evening'][lang]
            elif 22 < cur_hour < 4:
                response = self.bot_text['hello_night'][lang]
        response = response + ', ' + chat_name

        return self.response_formatter('text', response)

    def command_handler(self, update):
        commands = ['start', 'reverse', 'cat', 'dog']

        lang = update[self.message_key]['from']['language_code']
        in_text = update[self.message_key]['text']
        com_length = update[self.message_key]['entities'][0]['length']
        command = in_text[1:com_length]
        in_text = in_text[com_length:].strip()
        hello_msg = self.bot_text['start'][lang].format(update[self.message_key]['chat']['first_name'])

        if command == 'start':
            return self.response_formatter('text', hello_msg)
        elif command == 'reverse':
            return self.response_formatter('text', in_text[::-1])
        elif command == 'cat':
            img_url = self.get_cat('https://api.thecatapi.com/v1/images/search')
            return self.response_formatter('photo', img_url)
        elif command == 'dog':
            img_url = self.get_dog('https://random.dog/woof.json')
            return self.response_formatter('photo', img_url)
        else:
            return self.response_formatter('text', 'Unknown command')

    def send_message(self, chat_id, msg_id, bot_response):
        params = {'chat_id': chat_id, 'reply_to_message_id': msg_id, bot_response['type']: bot_response['resp']}
        method = bot_response['method']
        resp = requests.post(self.api_url + method, params)
        return resp
