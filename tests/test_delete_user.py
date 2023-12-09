# tests/test_delete_user.py
import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app.models import db, User
from app.app import app

class DeleteUserTest(unittest.TestCase):
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

    def test_delete_user_success(self):
        # Create a user for testing
        with self.app.app_context():
            test_user = User(username='john_doe', email='john@example.com')
            db.session.add(test_user)
            db.session.commit()

            # Check if the user is created successfully
            created_user = User.query.get(test_user.id)
            self.assertEqual(created_user, test_user)

        # Send a DELETE request to delete the user
        response = self.client.delete('/delete_user/'+str(created_user.id))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response message indicates successful deletion
        expected_success_response = jsonify({'message': 'User deleted successfully'})
        self.assertEqual(response.get_json(), expected_success_response.get_json())

        # Check if the user is actually deleted from the database
        with self.app.app_context():
            deleted_user = User.query.get(test_user.id)
            self.assertIsNone(deleted_user)

    def test_delete_user_nonexistent(self):
        # Send a DELETE request with a non-existent user ID
        response = self.client.delete('/delete_user/999')

        # Check if the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Check if the response JSON indicates that the user was not found
        expected_error_response = jsonify({'message': 'User not found'})
        self.assertEqual(response.get_json(), expected_error_response.get_json())

if __name__ == '__main__':
    unittest.main()
