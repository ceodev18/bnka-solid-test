# tests/test_get_user.py
import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app.models import db, User
from app.app import app

class GetUserTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_get_user_success(self):
        # Create a user for testing
        with self.app.app_context():
            test_user = User(username='john_doe', email='john@example.com')
            db.session.add(test_user)
            db.session.commit()

        # Send a GET request to retrieve the user details
        response = self.client.get('/get_user/1')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response JSON matches the expected user details
        expected_response = jsonify({'username': 'john_doe', 'email': 'john@example.com'})
        self.assertEqual(response.get_json(), expected_response.get_json())

    def test_get_user_not_found(self):
        # Send a GET request with an invalid user ID
        response = self.client.get('/get_user/1')

        # Check if the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Check if the response JSON indicates that the user was not found
        expected_response = jsonify({'message': 'User not found'})
        self.assertEqual(response.get_json(), expected_response.get_json())

if __name__ == '__main__':
    unittest.main()
