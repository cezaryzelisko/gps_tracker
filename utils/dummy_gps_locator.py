import time
from argparse import ArgumentParser

from src.auth import Auth
from src.device import Device
from src.gps_locator import RandomGPSLocator


def run_main_loop(interval):
    auth = Auth()
    device = Device('Random Device', auth)
    gps_locator = RandomGPSLocator(device.id, auth)

    print(f"Device: #{device.id} - '{device.name}' started!")

    try:
        while True:
            published_at, status_code = gps_locator.publish_new_coords()
            log(published_at, gps_locator.last_coords, status_code, gps_locator.device_id)
            time.sleep(interval)
    except KeyboardInterrupt:
        print('exiting...')


def log(published_at, coords, status_code, device_id):
    published_at_str = f'{published_at.year}-{published_at.month}-{published_at.day} ' \
                       f'{published_at.hour}:{published_at.minute}:{published_at.second}'

    print(f'[POST] -> '
          f'{published_at_str}, lat: {coords[0]:.3f}, lng: {coords[1]:.3f}, device_id: {device_id} -> '
          f'{status_code}')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--interval', '-i', type=int, default=30, help='Number of seconds between each packet')
    args = arg_parser.parse_args()

    run_main_loop(args.interval)
