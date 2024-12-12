from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from bson import ObjectId
from . import users_bp
from models.some_utility import insert_user, update_user, delete_user, users_collection


# Route to register a new user
@users_bp.route("/api/rehome/signup", methods=["POST"])
def register_user():
    try:
        data = request.json
        # Check if the email is already in use
        if users_collection.find_one({"email": data['email']}):
            return jsonify({'status': 'error', 'message': 'Email already in use'}), 400
        # Create a new user object
        user = {
            "user_id": str(ObjectId()),
            "username": data['username'],
            "email": data['email'],
            "password": generate_password_hash(data['password']),
            "profile_picture": data.get('profile_picture'),  # Use .get() to handle missing keys
            "postcode": data.get('postcode'),
            "phone_number": data.get('phone_number') ,   
            "items": [] # Initialize an empty list for the user's items
        }
        # Insert the new user into the database
        user_id, success = insert_user(user)
        if success:
            return make_response(jsonify({'status': 'success', 'user_id': user_id}), 201)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'Failed to register user'}), 500)
    except Exception as e:
        # Custom error message
        custom_message = f"Something went wrong: {str(e)}"
        return make_response(jsonify({'status': 'error', 'message': custom_message}), 500)
    
# Route to get a paginated list of users
@users_bp.route("/api/rehome/users", methods=["GET"])
@jwt_required()
def get_users():
    try:
        # Handle fetching a paginated list of users
        page_num, page_size = 1, 10
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        page_start = (page_size * (page_num - 1))
        data_to_return = []
        # Retrieve users from the database with pagination
        for user in users_collection.find().skip(page_start).limit(page_size):
            user['_id'] = str(user['_id'])
            data_to_return.append(user)
        return make_response(jsonify(data_to_return), 200)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)

# Route to update an existing user
@users_bp.route("/api/rehome/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    try:
        # Handle updating an existing user
        data = request.json
        # Update the user in the database
        success = update_user(user_id, data)
        if success:
            return make_response(jsonify({'status': 'User Successfully Updated'}), 200)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'Failed to update user'}), 500)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)

# Route to delete a user
@users_bp.route("/api/rehome/users/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    try:
        # Handle deleting a user
        success = delete_user(user_id)
        if success:
            return make_response(jsonify({'status': ' User successfully deleted'}), 200)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)