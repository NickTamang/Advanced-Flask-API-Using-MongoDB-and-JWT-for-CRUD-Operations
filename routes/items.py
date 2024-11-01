from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity  # Ensure these imports are included
from bson import ObjectId
from . import items_bp
from models.some_utility import insert_item, get_items, get_item_by_id, update_item, delete_item, get_items_by_partial_name

@items_bp.route("/api/rehome/items", methods=["POST"])
@jwt_required()
def share_item():
    data = request.json
    item = {
        "item_id": str(ObjectId()),
        "user_id": get_jwt_identity(),
        "item_name": data['item_name'],
        "description": data['description'],
        "photo_url": data['photo_url'],
        "status": data['status']
    }
    insert_item(item)
    return jsonify({'status': 'success'}), 201

@items_bp.route("/api/rehome/items", methods=["GET"])
@jwt_required()
def get_items_route():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    items = get_items(page_num, page_size)
    # Convert ObjectId to string
    for item in items:
        item['_id'] = str(item['_id'])
        item['item_id'] = str(item['item_id'])
    return jsonify(items), 200

@items_bp.route("/api/rehome/items/<item_id>", methods=["GET"])
def get_item_route(item_id):
    item = get_item_by_id(item_id)
    if item:
        item['_id'] = str(item['_id'])
        item['item_id'] = str(item['item_id'])
    return jsonify(item)


@items_bp.route("/api/rehome/items/name/<item_name_prefix>", methods=["GET"])
def get_items_by_partial_name_route(item_name_prefix):
    items = get_items_by_partial_name(item_name_prefix)
    for item in items:
        item['_id'] = str(item['_id'])
        item['item_id'] = str(item['item_id'])
    return jsonify(items), 200


@items_bp.route("/api/rehome/items/<item_id>", methods=["PATCH"])
@jwt_required()
def update_item_status(item_id):
    data = request.json
    update_item(item_id, {"status": data['status']})
    return jsonify({'status': 'success'}), 200

@items_bp.route("/api/rehome/items/<item_id>", methods=["DELETE"])
@jwt_required()
def delete_item_route(item_id):
    delete_item(item_id)
    return jsonify({'status': 'success'}), 200