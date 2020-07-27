from gps_tracker.gps_locator import RandomGPSLocator
from gps_tracker.runner import main


def get_gps_locator(auth, device):
    return RandomGPSLocator(device.id, auth, (51.005, 21.001))


if __name__ == '__main__':
    main(get_gps_locator)
