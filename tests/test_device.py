import unittest
from unittest import mock

from gps_tracker.auth import Auth
from gps_tracker.device import Device
from gps_tracker.tests.utils import set_up_mock_auth_post


class DeviceTests(unittest.TestCase):
    @classmethod
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def setUpClass(cls, mock_post):
        set_up_mock_auth_post(mock_post)
        cls.auth = Auth()

    @mock.patch('gps_tracker.device.parse_config')
    def test_can_set_up_device_id_from_config_file(self, mock_parser):
        config = {'device': {'id': 11}}
        mock_parser.return_value = config

        device = Device('Test Device', self.auth)

        self.assertIsInstance(device.id, int)
        self.assertEqual(device.id, config['device']['id'])

    @mock.patch('gps_tracker.device.Device.save_id')
    @mock.patch('gps_tracker.device.parse_config')
    @mock.patch('gps_tracker.utils.api_requests.requests.post')
    def test_can_set_up_device_id_from_api(self, mock_post, mock_parser, _):
        response = {'id': 10}
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = response

        mock_parser.return_value = {'device': {'id': None}}

        device = Device('Test Device', self.auth)

        self.assertIsInstance(device.id, int)
        self.assertEqual(device.id, response['id'])


if __name__ == '__main__':
    unittest.main()
