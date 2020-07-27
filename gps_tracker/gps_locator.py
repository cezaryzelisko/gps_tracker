import datetime
import random
from abc import abstractmethod

from gps_tracker.utils.api_requests import post


class GPSLocator:
    def __init__(self, device_id, auth, starting_coords=(0.0, 0.0)):
        self.device_id = device_id
        self.headers = auth.get_authorization_header()
        self.last_known_location = self.format_last_known_location_dict(*starting_coords)

    @staticmethod
    def format_last_known_location_dict(lat, lng, published_at=None):
        return {
            'published_at': published_at if published_at else datetime.datetime.now(),
            'lat': lat,
            'lng': lng
        }

    @abstractmethod
    def get_new_location(self):
        raise NotImplementedError

    def publish_new_location(self):
        self.last_known_location = self.get_new_location()
        body = {
            'lat': self.last_known_location['lat'],
            'lng': self.last_known_location['lng'],
            'published_at': self.get_formatted_datetime_str(self.last_known_location['published_at']),
            'device_id': self.device_id
        }
        status_code, _ = post('api', 'gps_footprint', body, additional_headers=self.headers)
        return self.last_known_location['published_at'], status_code

    @staticmethod
    def get_formatted_datetime_str(date_time):
        return f'{date_time.year}-{date_time.month}-{date_time.day} ' \
               f'{date_time.hour}:{date_time.minute}:{date_time.second}'


class RandomGPSLocator(GPSLocator):
    def get_new_location(self):
        abs_diff = 0.01
        new_latitude = self.last_known_location['lat'] + random.choice([-1, 1]) * abs_diff
        new_longitude = self.last_known_location['lng'] + random.choice([-1, 1]) * abs_diff
        return self.format_last_known_location_dict(new_latitude, new_longitude)
