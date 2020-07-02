import json
import os

CONFIG_NAME = 'config.json'


def get_config_path():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root_path, CONFIG_NAME)


def parse_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}
