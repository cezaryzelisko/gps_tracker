import os
import unittest

from gps_tracker.utils import config_parser


class TestConfigParser(unittest.TestCase):
    def test_can_get_configuration_path(self):
        config_path = config_parser.get_config_path()
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cp = os.path.join(root_path, config_parser.CONFIG_NAME)

        self.assertEqual(config_path, cp)

    def test_can_parse_configuration(self):
        config = config_parser.parse_config()
        self.assertIsInstance(config, dict)
        self.assertIn('endpoints', config)


if __name__ == '__main__':
    unittest.main()
