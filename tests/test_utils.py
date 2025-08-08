import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from utils import is_valid_url

class UtilsTestCase(unittest.TestCase):
    def test_valid_url(self):
        self.assertTrue(is_valid_url("https://example.com"))

    def test_invalid_url(self):
        self.assertFalse(is_valid_url("not-a-url"))
