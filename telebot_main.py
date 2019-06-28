import json


with open('config.json', 'r') as cfg_file:
    data = json.load(cfg_file)
print(data['token'])
