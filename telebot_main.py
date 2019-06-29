import json
import logging

import TeleBotHandler


def main():
    formatsring = '%(asctime)s %(levelname)s:%(message)s'
    dateformat = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename='bot.log', format=formatsring, datefmt=dateformat, level=logging.DEBUG)

    with open('config.json', 'r') as cfg_file:
        data = json.load(cfg_file)
    bot = TeleBotHandler.TeleBotHandler(data['token'])
    bot.get_updates()


if __name__ == '__main__':
    main()
