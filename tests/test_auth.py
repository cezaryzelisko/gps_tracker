import unittest
from unittest import mock

from gps_tracker.auth import Auth
from gps_tracker.tests.utils import set_up_mock_post


class TestAuth(unittest.TestCase):
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_get_authorization_header(self, mock_post):
        set_up_mock_post(mock_post)

        auth = Auth()
        auth_header = auth.get_authorization_header()

        self.assertIn('Authorization', auth_header)
        self.assertEqual(auth_header['Authorization'], 'Bearer access_token')


if __name__ == '__main__':
    unittest.main()
