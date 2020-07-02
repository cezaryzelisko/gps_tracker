import datetime
import unittest
from unittest import mock

from gps_tracker.gps_locator import RandomGPSLocator


class TestGPSLocator(unittest.TestCase):
    DEVICE_ID = 1

    @staticmethod
    def set_up_mock_post(mock_post):
        access_timestamp = int(datetime.datetime.now().timestamp())

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access': 'access_token',
            'refresh': 'refresh_token',
            'accessExpiresAt': access_timestamp,
            'refreshExpiresAt': access_timestamp + 3600
        }

        return mock_post

    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_form_authorization_headers(self, mock_post):
        self.set_up_mock_post(mock_post)

        gps_locator = RandomGPSLocator(self.DEVICE_ID)

        self.assertIsInstance(gps_locator.headers, dict)
        self.assertIn('Authorization', gps_locator.headers)

    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_get_new_coordinates(self, mock_post):
        self.set_up_mock_post(mock_post)

        gps_locator = RandomGPSLocator(self.DEVICE_ID)
        new_coords = gps_locator.get_new_coords()

        self.assertEqual(len(new_coords), 2)
        self.assertGreaterEqual(new_coords[0], -90)
        self.assertLessEqual(new_coords[0], 90)
        self.assertGreaterEqual(new_coords[1], -180)
        self.assertLessEqual(new_coords[1], 180)

    def test_can_publish_new_coordinates(self):
        with mock.patch('gps_tracker.utils.api_requests.requests.post') as auth_mock_post:
            self.set_up_mock_post(auth_mock_post)

            gps_locator = RandomGPSLocator(self.DEVICE_ID)

            with mock.patch('gps_tracker.utils.api_requests.requests.post') as gps_mock_post:
                gps_mock_post.return_value.status_code = 200
                _, status_code = gps_locator.publish_new_coords()

                self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()
