import json
import logging
import datetime
import time


import TeleBotHandler


def is_command(update):
    if 'entities' in update['message'] and update['message']['entities'][0]['type'] == 'bot_command':
        return True
    else:
        return False


def main():
    formatsring = '%(asctime)s %(levelname)s:%(message)s'
    dateformat = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename='bot.log', format=formatsring, datefmt=dateformat, level=logging.DEBUG)

    with open('config.json', 'r') as cfg_file:
        data = json.load(cfg_file)
    new_offset = None

    while True:
        time.sleep(1)
        bot = TeleBotHandler.TeleBotHandler(data['token'])
        updates_list = bot.get_updates(new_offset)
        for update in updates_list:
            cur_update_id = update['update_id']
            cur_chat_id = update['message']['chat']['id']

            if is_command(update):
                bot_response = bot.command_handler(update)
            else:
                bot_response = bot.request_handler(update)

            bot.send_message(cur_chat_id, bot_response)
            new_offset = cur_update_id + 1

        # print(new_offset, '\n', datetime.datetime.now().second)


if __name__ == '__main__':
    main()
