from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from . import comments_bp
from models.some_utility import insert_comment, get_comments, update_comment, delete_comment

# Route to add a new comment
@comments_bp.route("/api/rehome/comments", methods=["POST"])
@jwt_required()
def add_comment():
    data = request.json
    if 'item_id' not in data or 'comment_text' not in data:
        return make_response(jsonify({'status': 'error', 'message': 'Missing item_id or comment_text'}), 400)
    comment = {
        "comment_id": str(ObjectId()),
        "item_id": data['item_id'],
        "user_id": get_jwt_identity(),
        "comment_text": data['comment_text'],
        "timestamp": datetime.now().isoformat(),
        "reply": None
    }
    comment_id, success = insert_comment(comment)
    if success:
        return make_response(jsonify({'status': 'success', 'comment_id': comment_id}), 201)
    else:
        return make_response(jsonify({'status': 'error', 'message': 'Failed to add comment'}), 500)

# Route to get comments with pagination
@comments_bp.route("/api/rehome/comments", methods=["GET"])
@jwt_required()
def get_comments_route():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    comments, success = get_comments(page_num, page_size)
    if success:
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['comment_id'] = str(comment['comment_id'])
            comment['item_id'] = str(comment['item_id'])
            comment['user_id'] = str(comment['user_id'])
        return make_response(jsonify(comments), 200)
    else:
        return make_response(jsonify({'status': 'error', 'message': 'Failed to retrieve comments'}), 500)

# Route to edit an existing comment
@comments_bp.route("/api/rehome/comments/<comment_id>", methods=["PUT"])
@jwt_required()
def edit_comment(comment_id):
    data = request.json
    success = update_comment(comment_id, data)
    if success:
        return make_response(jsonify({'status': 'success'}), 200)
    else:
        return make_response(jsonify({'status': 'error', 'message': 'Comment not found'}), 404)

# Route to delete a comment
@comments_bp.route("/api/rehome/comments/<comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_route(comment_id):
    success = delete_comment(comment_id)
    if success:
        return make_response(jsonify({'status': 'success'}), 200)
    else:
        return make_response(jsonify({'status': 'error', 'message': 'Comment not found'}), 404)

# Route to reply to a comment
@comments_bp.route("/api/rehome/comments/<comment_id>/reply", methods=["POST"])
@jwt_required()
def reply_comment(comment_id):
    data = request.json
    success = update_comment(comment_id, {"reply": data['reply']})
    if success:
        return make_response(jsonify({'status': 'success'}), 200)
    else:
        return make_response(jsonify({'status': 'error', 'message': 'Comment not found'}), 404)