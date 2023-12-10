# app/routes.py
from flask import Blueprint, jsonify
from flask import request
from sqlalchemy.orm import Session
from .app import app, db
from .models import User
from flasgger import swag_from

main_bp = Blueprint('main', __name__)


# Create user
@main_bp.route('/create_user', methods=['POST'])
def create_user():
    """
    Create a new user.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: true
    responses:
      201:
        description: User created successfully
      400:
        description: Bad request, missing parameters or duplicate username/email
    """
    data = request.form
    
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Get user
@main_bp.route('/get_user/<int:user_id>', methods=['GET'])
@swag_from({
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
            },
        ],
        'responses': {
            200: {
                'description': 'User details',
                'content': {
                    'application/json': {
                        'example': {
                            'username': 'john_doe',
                            'email': 'john@example.com',
                        },
                    },
                },
            },
            404: {
                'description': 'User not found',
            },
        },
    })
def get_user(user_id):
    with Session(db.engine, expire_on_commit=False) as session:
        user = session.get(User, user_id)
        if user:
            return jsonify({'username': user.username, 'email': user.email})
        else:
            return jsonify({'message': 'User not found'}), 404

# Update user
@main_bp.route('/update_user/<int:user_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
        },
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': False,
        },
        {
            'name': 'email',
            'in': 'formData',
            'type': 'string',
            'required': False,
        }
    ],
    'responses': {
        200: {
            'description': 'User updated successfully',
        },
        404: {
            'description': 'User not found',
        },
    },
})
def update_user(user_id):
    with Session(db.engine, expire_on_commit=False) as session:
        user = session.get(User, user_id)
        if user:
            data = request.form

            # Update username if provided in the request
            if 'username' in data:
                user.username = data['username']

            # Update email if provided in the request
            if 'email' in data:
                user.email = data['email']
            session.commit()
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404

# Delete user
@main_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@swag_from({
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
            },
        ],
        'responses': {
            200: {
                'description': 'User deleted successfully',
            },
            404: {
                'description': 'User not found',
            },
        },
    })
def delete_user(user_id):
    # Use db.session to interact with the database
    with Session(db.engine, expire_on_commit=False) as session:
        user = session.get(User, user_id)
        if user:
            # Delete the user from the database
            session.delete(user)
            session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404


# Get all users
@main_bp.route('/get_all_users', methods=['GET'])
@swag_from({
        'responses': {
            200: {
                'description': 'List of all users',
                'content': {
                    'application/json': {
                        'example': {
                            'users': [
                                {
                                    'username': 'john_doe',
                                    'email': 'john@example.com',
                                },
                                {
                                    'username': 'alice',
                                    'email': 'alice@example.com',
                                },
                            ],
                        },
                    },
                },
            },
        },
    })
def get_all_users():
    users = User.query.all()
    user_list = [{'id':user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify({'users': user_list})
