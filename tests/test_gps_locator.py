import unittest
from unittest import mock

from gps_tracker.auth import Auth
from gps_tracker.gps_locator import RandomGPSLocator
from gps_tracker.tests.utils import set_up_mock_auth_post


class GPSLocatorTests(unittest.TestCase):
    DEVICE_ID = 1

    @classmethod
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def setUpClass(cls, mock_post):
        set_up_mock_auth_post(mock_post)
        cls.auth = Auth()

    def test_can_form_authorization_headers(self):
        gps_locator = RandomGPSLocator(self.DEVICE_ID, self.auth)

        self.assertIsInstance(gps_locator.headers, dict)
        self.assertIn('Authorization', gps_locator.headers)

    def test_can_get_new_coordinates(self):
        gps_locator = RandomGPSLocator(self.DEVICE_ID, self.auth)
        new_coords = gps_locator.get_new_coords()

        self.assertEqual(len(new_coords), 2)
        self.assertGreaterEqual(new_coords[0], -90)
        self.assertLessEqual(new_coords[0], 90)
        self.assertGreaterEqual(new_coords[1], -180)
        self.assertLessEqual(new_coords[1], 180)

    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_publish_new_coordinates(self, gps_mock_post):
        gps_locator = RandomGPSLocator(self.DEVICE_ID, self.auth)

        gps_mock_post.return_value.status_code = 201
        _, status_code = gps_locator.publish_new_coords()

        self.assertEqual(status_code, 201)


if __name__ == '__main__':
    unittest.main()
