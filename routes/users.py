from flask import request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from bson import ObjectId
from . import users_bp
from models.some_utility import insert_user, get_user_by_id, update_user, delete_user, users_collection

@users_bp.route("/api/rehome/users", methods=["POST"])
def register_user():
    data = request.json
    if users_collection.find_one({"email": data['email']}):
        return jsonify({'status': 'error', 'message': 'Email already in use'}), 400

    user = {
        "user_id": str(ObjectId()),
        "username": data['username'],
        "email": data['email'],
        "password": generate_password_hash(data['password']),
        "profile_picture": data['profile_picture'],
        "postcode": data['postcode'],
        "phone_number": data['phone_number']
    }
    insert_user(user)
    return jsonify({'status': 'success'}), 201


@users_bp.route("/api/rehome/users", methods=["GET"])
@jwt_required()
def get_users():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    data_to_return = []
    for user in users_collection.find().skip(page_start).limit(page_size):
        user['_id'] = str(user['_id'])
        data_to_return.append(user)
    return jsonify(data_to_return), 200

@users_bp.route("/api/rehome/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    data = request.json
    update_user(user_id, data)
    return jsonify({'status': 'success'}), 200

@users_bp.route("/api/rehome/users/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    delete_user(user_id)
    return jsonify({'status': 'success'}), 200