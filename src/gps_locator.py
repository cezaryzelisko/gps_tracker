import datetime
import random
from abc import abstractmethod

from gps_tracker.utils.api_requests import post


class GPSLocator:
    STARTING_COORDS = (51.005, 21.001)

    def __init__(self, device_id, auth):
        self.device_id = device_id
        self.headers = auth.get_authorization_header()
        self.last_coords = self.STARTING_COORDS

    @abstractmethod
    def get_new_coords(self):
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
    def get_new_coords(self):
        if self.last_coords is None:
            return random.randrange(-90, 90), random.randrange(-180, 180)
        else:
            abs_diff = 0.01
            new_latitude = self.last_coords[0] + random.choice([-1, 1]) * abs_diff
            new_longitude = self.last_coords[1] + random.choice([-1, 1]) * abs_diff
            return new_latitude, new_longitude
