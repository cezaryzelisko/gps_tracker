from gps_tracker.gps_locator import RandomGPSLocator
from gps_tracker.runner import main
from gps_tracker.auth import Auth
from gps_tracker.device import Device


if __name__ == '__main__':
    auth = Auth()
    device = Device('Random Device', auth)
    gps_locator = RandomGPSLocator(device.id, auth, (51.005, 21.001))
    
    main(gps_locator, device)
