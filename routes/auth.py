from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash
from . import auth_bp
from models.some_utility import get_user_by_email, get_user_by_id
from token_utils import add_token_to_blocklist

# Generate new tokens function
def generate_tokens(user_id):
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    return access_token, refresh_token

@auth_bp.route("/api/rehome/login", methods=["POST"], endpoint="auth_login")
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = get_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        access_token, refresh_token = generate_tokens(user['user_id'])
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify({'msg': 'Wrong email or password'}), 401

@auth_bp.route("/api/rehome/logout", methods=["POST"], endpoint="auth_logout")
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    expires_in = get_jwt()['exp'] - get_jwt()['iat']  # Calculate the token's remaining time to liv
    add_token_to_blocklist(jti, expires_in)
    return jsonify({'msg': 'Successfully logged out. Token has been revoked.'}), 200

@auth_bp.route("/api/rehome/whois", methods=["GET"], endpoint="auth_protected")
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    if user:
        return jsonify(logged_in_as=user['username']), 200
    return jsonify({'msg': 'User not found'}), 404