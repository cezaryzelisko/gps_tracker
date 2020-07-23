import time

from RPi import GPIO
from gps_tracker.gps_locator import GPSLocator
from gps_tracker.serial_connection import SerialConnection
from gps_tracker.wave_share_config import WaveShareGPS


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


if __name__ == '__main__':
    with SerialConnection(WaveShareGPS.DEFAULT_DEVICE) as serial_conn:
        with WaveShareGPSLocator(1, None, serial_conn) as ws_gps:
            ws_gps.get_new_coords()
