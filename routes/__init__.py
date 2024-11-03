from flask import Blueprint

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# Create a Blueprint for user-related routes
users_bp = Blueprint('users', __name__)

# Create a Blueprint for item-related routes
items_bp = Blueprint('items', __name__)

# Create a Blueprint for comment-related routes
comments_bp = Blueprint('comments', __name__)


from . import auth, users, items, comments