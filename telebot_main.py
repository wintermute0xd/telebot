import json
import logging

import TeleBotHandler


def main():
    formatsring = '%(asctime)s %(levelname)s:%(message)s'
    dateformat = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename='bot.log', format=formatsring, datefmt=dateformat, level=logging.DEBUG)

    with open('config.json', 'r') as cfg_file:
        data = json.load(cfg_file)
    new_offset = None

    while True:
        bot = TeleBotHandler.TeleBotHandler(data['token'])
        updates_list = bot.get_updates(new_offset)
        for update in updates_list:
            cur_update_id = update['update_id']
            cur_chat_id = update['message']['chat']['id']

            bot_response = bot.request_handler(update)
            bot.send_message(cur_chat_id, bot_response)
            new_offset = cur_update_id + 1

        print(new_offset, '\n')


if __name__ == '__main__':
    main()
