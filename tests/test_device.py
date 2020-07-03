import unittest
from unittest import mock

from gps_tracker.auth import Auth
from gps_tracker.device import Device
from gps_tracker.tests.utils import set_up_mock_post
from gps_tracker.utils.config_parser import parse_config


class TestDevice(unittest.TestCase):
    @classmethod
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def setUpClass(cls, mock_post):
        set_up_mock_post(mock_post)
        cls.auth = Auth()

    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_set_up_device_id(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'id': 1}

        device = Device('Test Device', self.auth)

        config = parse_config()

        self.assertIsInstance(device.id, int)
        self.assertGreaterEqual(device.id, 1)
        self.assertEqual(config['device']['id'], 1)


if __name__ == '__main__':
    unittest.main()
