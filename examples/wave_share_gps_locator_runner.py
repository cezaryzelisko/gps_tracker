from gps_tracker.runner import main
from gps_tracker.serial_connection import SerialConnection
from gps_tracker.wave_share_config import WaveShareGPS
from gps_tracker.wave_share_gps_locator import WaveShareGPSLocator
from gps_tracker.auth import Auth
from gps_tracker.device import Device
            

if __name__ == '__main__':
    auth = Auth()
    device = Device('WaveShare Device', auth)
    
    with SerialConnection(WaveShareGPS.DEFAULT_DEVICE) as serial_conn:
        with WaveShareGPSLocator(device.id, auth, serial_conn) as ws_gps:
            enabled = ws_gps.wait_for_gps()
            if enabled:
                main(ws_gps, device)
            else:
                print('ERROR: unable to initialize GPS.')
