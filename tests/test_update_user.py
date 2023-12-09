# tests/test_update_user.py
import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app.models import db, User
from sqlalchemy.orm import Session

from app.app import app

class UpdateUserTest(unittest.TestCase):
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

    def test_update_user_success(self):
        # Create a user for testing
        with self.app.app_context():
            test_user = User(username='john_doe', email='john@example.com')
            db.session.add(test_user)
            db.session.commit()

        # Send a PUT request to update the user
        response = self.client.put('/update_user/1', data={'username': 'john_updated', 'email': 'updated@example.com'})

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response message indicates successful update
        expected_response = jsonify({'message': 'User updated successfully'})
        self.assertEqual(response.get_json(), expected_response.get_json())

        # Check if the user is actually updated in the database
        with self.app.app_context(), Session(db.engine, expire_on_commit=False) as session:
            updated_user = session.get(User, 1)
            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.username, 'john_updated')
            self.assertEqual(updated_user.email, 'updated@example.com')
    
    def test_update_user_not_found(self):
        # Send a PUT request with an invalid user ID
        updated_data = {'username': 'john_updated', 'email': 'updated@example.com'}
        response = self.client.put('/update_user/1', json=updated_data)

        # Check if the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Check if the response JSON indicates that the user was not found
        expected_response = jsonify({'message': 'User not found'})
        self.assertEqual(response.get_json(), expected_response.get_json())

if __name__ == '__main__':
    unittest.main()
