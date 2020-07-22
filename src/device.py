from gps_tracker.utils.api_requests import post
from gps_tracker.utils.config_parser import parse_config, update_config


class Device:
    def __init__(self, name, auth):
        self.name = name
        self.headers = auth.get_authorization_header()
        self.id = self.get_id()

    def get_id(self):
        device_id, config = self.parse_id_from_config()
        if device_id is None:
            device_id = self.get_new_id_from_api()
            self.save_id(config, device_id)

        return device_id

    @staticmethod
    def parse_id_from_config():
        config = parse_config()
        if 'device' in config and 'id' in config['device']:
            return config['device']['id'], config
        return None, config

    def get_new_id_from_api(self):
        status_code, data = post('api', 'device', {'name': self.name}, additional_headers=self.headers)
        if status_code == 201:
            return data['id']
        else:
            raise ValueError('Unable to create new device. Check your connection to the API.')

    @staticmethod
    def save_id(config, device_id):
        config['device']['id'] = device_id
        update_config(config)
