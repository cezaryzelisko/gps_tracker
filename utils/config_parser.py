import json
import os

CONFIG_NAME = 'config.json'


def parse_config():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_path, CONFIG_NAME)
    with open(config_path, 'r') as config_file:
        return json.load(config_file)
