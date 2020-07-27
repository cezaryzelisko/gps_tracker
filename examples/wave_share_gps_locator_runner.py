from gps_tracker.runner import main
from gps_tracker.serial_connection import SerialConnection
from gps_tracker.wave_share_config import WaveShareGPS
from gps_tracker.wave_share_gps_locator import WaveShareGPSLocator


def get_gps_locator(auth, device):
    with SerialConnection(WaveShareGPS.DEFAULT_DEVICE) as serial_conn:
        with WaveShareGPSLocator(device.id, auth, serial_conn) as ws_gps:
            enabled = ws_gps.wait_for_gps()
            if enabled:
                return ws_gps
            else:
                print('ERROR: unable to initialize GPS.')


if __name__ == '__main__':
    main(get_gps_locator)
