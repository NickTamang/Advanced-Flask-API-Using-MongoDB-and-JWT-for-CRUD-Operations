from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash
from . import auth_bp
from models.some_utility import get_user_by_email, get_user_by_id
from token_utils import add_token_to_blocklist
from flask_cors import cross_origin

# Function to generate new access and refresh tokens
def generate_tokens(user_id):
    # Create access and refresh tokens for the given user ID
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    return access_token, refresh_token

# Route for user login
@auth_bp.route("/api/rehome/login", methods=["POST", "OPTIONS"], endpoint="auth_login")
@cross_origin(origin='http://localhost:4200')
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        # Handle user login and return JWT tokens if credentials are valid
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user, success = get_user_by_email(email)
        if success and check_password_hash(user['password'], password):
            access_token, refresh_token = generate_tokens(user['user_id'])
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        return jsonify({'msg': 'Wrong email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for user logout
@auth_bp.route("/api/rehome/logout", methods=["POST", "OPTIONS"], endpoint="auth_logout")
@cross_origin(origin='http://localhost:4200')
@jwt_required()
def logout():
    try:
        # Handle user logout and add the token to the blocklist
        jti = get_jwt()['jti']
        expires_in = get_jwt()['exp'] - get_jwt()['iat']
        add_token_to_blocklist(jti, expires_in)
        return jsonify({'msg': 'Successfully logged out. Token has been revoked.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get information about the logged-in user
@auth_bp.route("/api/rehome/whois", methods=["GET", "OPTIONS"], endpoint="auth_protected")
@cross_origin(origin='http://localhost:4200')
@jwt_required()
def protected():
    try:
        # Return information about the currently logged-in user
        current_user_id = get_jwt_identity()
        user, success = get_user_by_id(current_user_id)
        if success:
            return jsonify(logged_in_as=user['username']), 200
        return jsonify({'msg': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Route to get the profile picture of the logged-in user
@auth_bp.route("/api/rehome/howisuser", methods=["GET", "OPTIONS"], endpoint="auth_profile_picture")
@cross_origin(origin='http://localhost:4200')
@jwt_required()
def get_profile_picture():
    try:
        # Return the profile picture of the currently logged-in user
        current_user_id = get_jwt_identity()
        user, success = get_user_by_id(current_user_id)
        if success:
            return jsonify(profile_picture=user['profile_picture']), 200
        return jsonify({'msg': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500