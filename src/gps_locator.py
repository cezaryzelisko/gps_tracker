import datetime
import random
import time
from abc import abstractmethod

import RPi.GPIO as GPIO
from gps_tracker.utils.api_requests import post
from src.wave_share_config import WaveShareGPS


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


class WaveShareGPSLocator(GPSLocator):
    def __init__(self, device_id, auth, serial_conn):
        super().__init__(device_id, auth)
        self.serial_conn = serial_conn

    def __enter__(self):
        self.power_on()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.power_down()

    def power_on(self):
        print(f'{WaveShareGPS.NAME} is starting...', end='\t')
        self.setup_power_pin()
        self.set_power_pin_state(break_timeout=2)
        self.serial_conn.flush_input()
        print(f'{WaveShareGPS.NAME} is ready')
        self.wait_for_gps()

    def power_down(self):
        print(f'{WaveShareGPS.NAME} is logging off...', end='\t')
        self.set_power_pin_state(break_timeout=3)
        GPIO.cleanup()
        print('Good bye')

    @staticmethod
    def setup_power_pin():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(WaveShareGPS.POWER_PIN, GPIO.OUT)
        time.sleep(0.1)

    @staticmethod
    def set_power_pin_state(break_timeout):
        GPIO.output(WaveShareGPS.POWER_PIN, GPIO.HIGH)
        time.sleep(break_timeout)
        GPIO.output(WaveShareGPS.POWER_PIN, GPIO.LOW)
        time.sleep(2)

    def wait_for_gps(self, timeout=10):
        print('Start GPS session...')
        self.serial_conn.send_at(WaveShareGPS.POWER_ON_CMD, WaveShareGPS.POWER_ON_CMD_RESPONSE, 1)
        time.sleep(2)

        start = time.time()
        while (time.time() - start) < timeout:
            coords = self.get_new_coords()
            if coords == (-1, -1):
                print('Waiting for GPS to initialize...')
            else:
                print('GPS initialized')
                break
        else:
            self.serial_conn.send_at(WaveShareGPS.POWER_OFF_CMD, WaveShareGPS.POWER_OFF_CMD_RESPONSE, 1)
            print('GPS is not ready')

    def get_new_coords(self):
        res_status, res_msg = self.serial_conn.send_at(
            WaveShareGPS.GPS_INFORMATION_CMD,
            WaveShareGPS.GPS_INFORMATION_CMD_RESPONSE,
            timeout=1
        )
        if res_status:
            if ',,,,,,' in res_msg:
                print('GPS is not ready')
                return -1, -1
            print(f'GPS:\t{res_msg}')
            return 0, 0
        else:
            print(f'ERROR:\t{res_msg}')
            return -1, -1
