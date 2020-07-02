import datetime
import unittest
from unittest import mock

from gps_tracker.auth import Auth


class TestAuth(unittest.TestCase):
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_get_authorization_header(self, mock_post):
        accessTimestamp = int(datetime.datetime.now().timestamp())

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access': 'access_token',
            'refresh': 'refresh_token',
            'accessExpiresAt': accessTimestamp,
            'refreshExpiresAt': accessTimestamp + 3600
        }

        auth = Auth()
        auth_header = auth.get_authorization_header()

        self.assertIn('Authorization', auth_header)
        self.assertEqual(auth_header['Authorization'], 'Bearer access_token')


if __name__ == '__main__':
    unittest.main()
