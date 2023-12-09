# tests/test_create_user.py
import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app.models import db, User
from app.app import app

class CreateUserTest(unittest.TestCase):
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

    def test_create_user(self):
        # Send a POST request to create a new user
        response = self.client.post('/create_user', data={'username': 'test_user', 'email': 'test@example.com'})

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Check if the response message is correct
        expected_response = jsonify({'message': 'User created successfully'})
        self.assertEqual(response.get_json(), expected_response.get_json())

        # Check if the user is actually created in the database
        with self.app.app_context():
            user = User.query.filter_by(username='test_user').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
