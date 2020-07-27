import time

from RPi import GPIO
from gps_tracker.gps_locator import GPSLocator
from gps_tracker.wave_share_config import WaveShareGPS


class WaveShareGPSLocator(GPSLocator):
    def __init__(self, device_id, auth, serial_conn):
        super().__init__(device_id, auth, (-1, -1))
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

    def power_down(self):
        print(f'{WaveShareGPS.NAME} is logging off...', end='\t')
        self.serial_conn.send_at(WaveShareGPS.POWER_OFF_CMD, WaveShareGPS.POWER_OFF_CMD_RESPONSE, 1)
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
            location = self.get_new_location()
            if location['lat'] == -1 and location['lng'] == -1:
                print('Waiting for GPS to initialize...')
            else:
                print('GPS initialized')
                return True
        
        print('GPS is not ready')
        return False

    def get_new_location(self):
        res_status, res_msg = self.serial_conn.send_at(
            WaveShareGPS.GPS_INFORMATION_CMD,
            WaveShareGPS.GPS_INFORMATION_CMD_RESPONSE,
            timeout=1
        )
        if res_status:
            if ',,,,,,' in res_msg:
                print('ERROR:\tGPS is not ready')
                return self.format_last_known_location_dict(-1, -1)
            datetime_str, lat, lng = self.parse_gps_information(res_msg)
            return self.format_last_known_location_dict(lat, lng)
        else:
            print(f'ERROR:\t{res_msg}')
            return self.format_last_known_location_dict(-1, -1)

    @staticmethod
    def parse_gps_information(information):
        gps_info_parts = information.split(',', 5)
        datetime_str, lat, lng = gps_info_parts[2:5]

        return datetime_str, lat, lng
