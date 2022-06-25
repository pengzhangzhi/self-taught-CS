import unittest
import unittest.mock

import load

class TestLoad(unittest.TestCase):

    def test_load_config_lowercased(self):
        with self.assertRaises(Exception) as context:
          load.load_config('remove_indexes')
        self.assertIn('remove_indexes.yaml', str(context.exception))

    def test_load_config_camelcased(self):
        with self.assertRaises(Exception) as context:
          load.load_config('SmartFridge')
        # Make sure it lowercases the file name
        self.assertIn('smartfridge.yaml', str(context.exception))


if __name__ == '__main__':
    unittest.main()
