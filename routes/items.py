from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity  
from bson import ObjectId
from . import items_bp
from models.some_utility import insert_item, get_items, get_item_by_id, update_item, delete_item, get_items_by_partial_name

#done Route to share a new item
@items_bp.route("/api/rehome/items", methods=["POST"])
@jwt_required()
def share_item():
    try:
        # Handle sharing a new item
        data = request.json
        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        item = {
            "item_id": str(ObjectId()),
            "user_id": user_id,
            "item_name": data['item_name'],
            "description": data['description'],
            "photo_url": data['photo_url'],
            "status": data['status'],
            "comments": []  # Initialize with an empty list of comments
        }
        item_id, success = insert_item(user_id, item)  # Pass user_id to associate the item with the user
        if success:
            return make_response(jsonify({'status': 'success', 'item_id': item_id}), 201)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'Failed to insert item'}), 500)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)

# Route to get a paginated list of items
@items_bp.route("/api/rehome/items", methods=["GET"])
@jwt_required()
def get_items_route():
    try:
        # Handle fetching a paginated list of items
        page_num, page_size = 1, 10
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))
        items, success = get_items(page_num, page_size)
        if success:
            for item in items:
                item['_id'] = str(item['_id'])
                item['item_id'] = str(item['item_id'])
            return make_response(jsonify(items), 200)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'Failed to retrieve items'}), 500)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)

# Route to get a specific item by its ID
@items_bp.route("/api/rehome/items/<item_id>", methods=["GET"])
@jwt_required()
def get_item_route(item_id):
    try:
        # Handle fetching a specific item by its ID
        item, success = get_item_by_id(item_id)
        if success:
            item['_id'] = str(item['_id'])
            item['item_id'] = str(item['item_id'])
            return make_response(jsonify(item), 200)
        else:
            return make_response(jsonify({"error": "Item not found"}), 404)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)
    

# Route to get items by partial name match
@items_bp.route("/api/rehome/items/name/<item_name_prefix>", methods=["GET"])
def get_items_by_partial_name_route(item_name_prefix):
    try:
        items, success = get_items_by_partial_name(item_name_prefix)
        if success:
            for item in items:
                item['_id'] = str(item['_id'])
                item['item_id'] = str(item['item_id'])
            return make_response(jsonify(items), 200)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'Failed to retrieve items'}), 500)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)

    
# Route to update the status of an item
@items_bp.route("/api/rehome/items/<item_id>", methods=["PATCH"])
@jwt_required()
def update_item_status(item_id):
    try:
        # Handle updating the status of an item
        data = request.json
        if 'status' not in data:
            return make_response(jsonify({"error": "Status not provided"}), 400)
        success = update_item(item_id, {"status": data['status']})
        if success:
            return make_response(jsonify({'status': 'Item Status Successfully Updated'}), 200)
        else:
            return make_response(jsonify({'status': 'error', 'message': 'Failed to update item'}), 500)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)

# Route to delete an item
@items_bp.route("/api/rehome/items/<item_id>", methods=["DELETE"])
@jwt_required()
def delete_item_route(item_id):
    try:
        # Handle deleting an item
        success = delete_item(item_id)
        if success:
            return make_response(jsonify({'status': 'Item Permanently Deleted'}), 200)
        else:
            return make_response(jsonify({"error": "Item not found"}), 404)
    except Exception as e:
        return make_response(jsonify({'status': 'error', 'message': str(e)}), 500)