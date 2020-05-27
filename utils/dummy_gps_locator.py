import datetime
import random
import time
from argparse import ArgumentParser

import requests

from gps_tracker.utils.config_parser import parse_config

STARTING_COORDS = (51.005, 21.001)
DEVICE_ID = 1


def get_csrf_token(config):
    csrf_token_endpoint = '/'.join([config['api_root'], config['endpoints']['gps_footprint']])
    response = requests.get(csrf_token_endpoint)
    return response.cookies['csrftoken']


def get_new_coords(abs_diff=0.01, prev_coords=None):
    if prev_coords is None:
        return random.randrange(-90, 90), random.randrange(-180, 180)
    else:
        assert abs_diff > 0, 'When previous coordinates are specified then abs_diff argument must be set'
        return prev_coords[0] + random.choice([-1, 1]) * abs_diff, prev_coords[1] + random.choice([-1, 1]) * abs_diff


def publish_new_coords(interval, config, csrf_token=None):
    coords = STARTING_COORDS
    gps_endpoint = '/'.join([config['api_root'], config['endpoints']['gps_footprint']])
    if csrf_token:
        headers = {'X-CSRFToken': csrf_token}
        cookies = {'csrftoken': csrf_token}
    else:
        headers = None
        cookies = None
    try:
        while True:
            coords = get_new_coords(prev_coords=coords)
            published_at = datetime.datetime.now()
            published_at_str = f'{published_at.year}-{published_at.month}-{published_at.day} ' \
                               f'{published_at.hour}:{published_at.minute}:{published_at.second}'
            body = {
                'lat': coords[0],
                'lng': coords[1],
                'published_at': published_at_str,
                'device_id': DEVICE_ID
            }
            response = requests.post(gps_endpoint, body, headers=headers, cookies=cookies)
            print(f'[POST] -> '
                  f'{published_at_str}, lat: {coords[0]:.3f}, lng: {coords[1]:.3f}, device_id: {DEVICE_ID} -> '
                  f'{response.status_code}')
            time.sleep(interval)
    except KeyboardInterrupt:
        print('exiting...')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--interval', '-i', type=int, default=30, help='Number of seconds between each packet')
    args = arg_parser.parse_args()

    config = parse_config()

    # csrf_token = get_csrf_token(config)

    publish_new_coords(args.interval, config)
