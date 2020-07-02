import datetime
import random

from gps_tracker.auth import Auth
from gps_tracker.utils.api_requests import post


class GPSLocator:
    STARTING_COORDS = (51.005, 21.001)

    def __init__(self, device_id):
        self.device_id = device_id
        self.auth = Auth()
        self.headers = self.auth.get_authorization_header()
        self.last_coords = self.STARTING_COORDS

    def get_new_coords(self, abs_diff=0.01):
        raise NotImplementedError

    def publish_new_coords(self):
        self.last_coords = self.get_new_coords()
        published_at = datetime.datetime.now()
        published_at_str = f'{published_at.year}-{published_at.month}-{published_at.day} ' \
                           f'{published_at.hour}:{published_at.minute}:{published_at.second}'
        body = {
            'lat': self.last_coords[0],
            'lng': self.last_coords[1],
            'published_at': published_at_str,
            'device_id': self.device_id
        }
        status_code, _ = post('api', 'gps_footprint', body, additional_headers=self.headers)
        return published_at, status_code


class RandomGPSLocator(GPSLocator):
    def get_new_coords(self, abs_diff=0.01):
        if self.last_coords is None:
            return random.randrange(-90, 90), random.randrange(-180, 180)
        else:
            assert abs_diff > 0, 'When previous coordinates are specified then abs_diff argument must be set'
            new_latitude = self.last_coords[0] + random.choice([-1, 1]) * abs_diff
            new_longitude = self.last_coords[1] + random.choice([-1, 1]) * abs_diff
            return new_latitude, new_longitude
