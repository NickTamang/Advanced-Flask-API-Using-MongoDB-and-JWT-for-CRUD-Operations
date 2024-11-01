from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)
items_bp = Blueprint('items', __name__)
comments_bp = Blueprint('comments', __name__)

from . import auth, users, items, comments