import unittest
from unittest import mock

from gps_tracker.utils import api_requests


class TestApiRequests(unittest.TestCase):
    def test_can_get_url(self):
        gps_footprint_url = api_requests.get_url('api', 'gps_footprint')
        self.assertEqual(gps_footprint_url, 'http://127.0.0.1:8000/api/gps-footprint/')

    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_obtain_token(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access': 'access_token',
            'refresh': 'refresh_token',
            'accessExpiresAt': 1593687701,
            'refreshExpiresAt': 1593687901
        }

        status_code, data = api_requests.obtain_token('test_user', 'test_password')

        self.assertEqual(status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIn('access', data)
        self.assertIn('refresh', data)
        self.assertIn('accessExpiresAt', data)
        self.assertIn('refreshExpiresAt', data)

    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_refresh_token(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'refresh': 'refresh_token',
            'refreshExpiresAt': 1593687901
        }

        status_code, data = api_requests.refresh_token('refresh_token')

        self.assertEqual(status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertIn('refresh', data)
        self.assertIn('refreshExpiresAt', data)


if __name__ == '__main__':
    unittest.main()
