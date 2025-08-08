import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app, db

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    def test_shorten_url(self):
        response = self.app.post('/shorten', json={"url": "https://example.com"})
        self.assertEqual(response.status_code, 201)

    def test_invalid_url(self):
        response = self.app.post('/shorten', json={"url": "invalid-url"})
        self.assertEqual(response.status_code, 400)
