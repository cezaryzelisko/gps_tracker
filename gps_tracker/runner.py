import time
from argparse import ArgumentParser


def main(gps_locator, device):
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--interval', '-i', type=int, default=30, help='Number of seconds between each packet')
    args = arg_parser.parse_args()

    run_main_loop(gps_locator, device, args.interval)


def run_main_loop(gps_locator, device, interval):
    print(f"Device: #{device.id} - '{device.name}' started!")

    try:
        while True:
            published_at, status_code = gps_locator.publish_new_location()
            log(gps_locator.get_formatted_datetime_str(published_at),
                gps_locator.last_known_location,
                status_code,
                gps_locator.device_id)
            time.sleep(interval)
    except KeyboardInterrupt:
        print('exiting...')


def log(published_at_str, location, status_code, device_id):
    print(f'[POST] -> '
          f'{published_at_str}, lat: {location["lat"]:.3f}, lng: {location["lng"]:.3f}, device_id: {device_id} -> '
          f'{status_code}')
