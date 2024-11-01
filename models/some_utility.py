from pymongo import MongoClient
from config import Config
import re

# Initialize MongoDB client and database
client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()

# Collections
users_collection = db.users
items_collection = db.items
comments_collection = db.comments

def get_user_by_email(email):
    return users_collection.find_one({'email': email})

def get_user_by_id(user_id):
    return users_collection.find_one({'user_id': user_id})

def insert_user(user_data):
    return users_collection.insert_one(user_data)

def update_user(user_id, update_data):
    return users_collection.update_one({'user_id': user_id}, {'$set': update_data})

def delete_user(user_id):
    return users_collection.delete_one({'user_id': user_id})

def get_items(page_num, page_size):
    skip = (page_num - 1) * page_size
    items_cursor = items_collection.find().skip(skip).limit(page_size)
    items = list(items_cursor)
    return items
def get_item_by_id(item_id):
    return items_collection.find_one({'item_id': item_id})

def get_items_by_partial_name(item_name_prefix):
    regex = re.compile(f'^{item_name_prefix}', re.IGNORECASE)
    items_cursor = items_collection.find({'item_name': regex})
    items = list(items_cursor)
    return items

def insert_item(item_data):
    return items_collection.insert_one(item_data)

def update_item(item_id, update_data):
    return items_collection.update_one({'item_id': item_id}, {'$set': update_data})

def delete_item(item_id):
    return items_collection.delete_one({'item_id': item_id})

def get_comments(page_num, page_size):
    skip = (page_num - 1) * page_size
    comments_cursor = comments_collection.find().skip(skip).limit(page_size)
    comments = list(comments_cursor)
    return comments

def get_comment_by_id(comment_id):
    return comments_collection.find_one({'comment_id': comment_id})

def insert_comment(comment_data):
    return comments_collection.insert_one(comment_data)

def update_comment(comment_id, update_data):
    return comments_collection.update_one({'comment_id': comment_id}, {'$set': update_data})

def delete_comment(comment_id):
    return comments_collection.delete_one({'comment_id': comment_id})