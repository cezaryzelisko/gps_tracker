import unittest
from unittest import mock

from gps_tracker.auth import Auth
from gps_tracker.tests.utils import set_up_mock_auth_post, set_up_mock_credentials


class AuthTests(unittest.TestCase):
    @mock.patch('gps_tracker.auth.Auth.parse_credentials')
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_get_authorization_header(self, mock_post, mock_credentials):
        set_up_mock_auth_post(mock_post)
        set_up_mock_credentials(mock_credentials)

        auth = Auth()
        auth_header = auth.get_authorization_header()

        self.assertIn('Authorization', auth_header)
        self.assertEqual(auth_header['Authorization'], 'Bearer access_token')


if __name__ == '__main__':
    unittest.main()
