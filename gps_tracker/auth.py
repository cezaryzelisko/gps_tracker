import json
import pkgutil
from datetime import datetime

from gps_tracker.utils.api_requests import obtain_token, refresh_token


class Auth:
    def __init__(self):
        self.tokens = {
            'access': '',
            'refresh': '',
            'accessExpiresAt': 0,
            'refreshExpiresAt': 0
        }
        self.tokens_date = datetime.now()
        self.credentials = self.parse_credentials()

        self.update_access_token()

    @staticmethod
    def parse_credentials():
        raw_credentials = pkgutil.get_data('gps_tracker', '../credentials.json')
        return json.loads(raw_credentials)

    def update_access_token(self):
        now = datetime.now()
        current_lifetime = (now - self.tokens_date).seconds * 0.9
        access_token_lifetime = int(now.timestamp() - self.tokens['accessExpiresAt'])
        refresh_token_lifetime = int(now.timestamp() - self.tokens['refreshExpiresAt'])

        if not self.tokens['access'] or current_lifetime > refresh_token_lifetime:
            status_code, self.tokens = obtain_token(self.credentials['username'], self.credentials['password'])
            self.tokens_date = datetime.now()
        elif access_token_lifetime < current_lifetime < refresh_token_lifetime:
            status_code, self.tokens['access'] = refresh_token(self.tokens['refresh'])
        else:
            return

        if status_code != 200:
            raise ValueError('Error occurred while obtaining the token. '
                             'Please check your credentials or Internet connection.')

    def get_authorization_header(self):
        return {'Authorization': f"Bearer {self.tokens['access']}"}
