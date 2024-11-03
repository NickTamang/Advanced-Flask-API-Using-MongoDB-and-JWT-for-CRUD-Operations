from pymongo import MongoClient
from config import Config
import re

# Initializing MongoDB client and database
client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()

# Collections
users_collection = db.users
items_collection = db.items
comments_collection = db.comments

# Retrieve a user by email
def get_user_by_email(email):
    try:
        # Find a user in the users collection by their email address
        user = users_collection.find_one({'email': email})
        if user:
            return user, True
        return None, False
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, False

# Retrieve a user by user ID
def get_user_by_id(user_id):
    try:
        # Find a user in the users collection by their user ID
        user = users_collection.find_one({'user_id': user_id})
        if user:
            return user, True
        return None, False
    except Exception as e:
        return None, False

# Insert a new user into the collection
def insert_user(user_data):
    try:
        # Add a new user to the users collection
        result = users_collection.insert_one(user_data)
        if result.inserted_id:
            return str(result.inserted_id), True  # Convert ObjectId to string
        return None, False
    except Exception as e:
        return None, False

# Update an existing user in the collection
def update_user(user_id, update_data):
    try:
        # Update the details of an existing user in the users collection
        result = users_collection.update_one({'user_id': user_id}, {'$set': update_data})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        return False

# Delete a user from the collection
def delete_user(user_id):
    try:
        # Remove a user from the users collection
        result = users_collection.delete_one({'user_id': user_id})
        if result.deleted_count > 0:
            return True
        return False
    except Exception as e:
        return False

# Retrieve a paginated list of items
def get_items(page_num, page_size):
    try:
        # Get a list of items from the items collection with pagination
        skip = (page_num - 1) * page_size
        items_cursor = items_collection.find().skip(skip).limit(page_size)
        items = list(items_cursor)
        return items, True
    except Exception as e:
        return [], False

# Retrieve an item by item ID
def get_item_by_id(item_id):
    try:
        # Find an item in the items collection by its item ID
        item = items_collection.find_one({'item_id': item_id})
        if item:
            return item, True
        return None, False
    except Exception as e:
        return None, False

# Retrieve items by partial name match
def get_items_by_partial_name(item_name_prefix):
    try:
        # Find items in the items collection that match the given name prefix
        regex = re.compile(f'^{item_name_prefix}', re.IGNORECASE)
        items_cursor = items_collection.find({'item_name': regex})
        items = list(items_cursor)
        return items, True
    except Exception as e:
        return [], False

# Insert a new item into the collection
def insert_item(item_data):
    try:
        # Add a new item to the items collection
        result = items_collection.insert_one(item_data)
        if result.inserted_id:
            return str(result.inserted_id), True
        return None, False
    except Exception as e:
        return None, False

# Update an existing item in the collection
def update_item(item_id, update_data):
    try:
        # Update the details of an existing item in the items collection
        result = items_collection.update_one({'item_id': item_id}, {'$set': update_data})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        return False

# Delete an item from the collection
def delete_item(item_id):
    try:
        # Remove an item from the items collection
        result = items_collection.delete_one({'item_id': item_id})
        if result.deleted_count > 0:
            return True
        return False
    except Exception as e:
        return False

# Retrieve a paginated list of comments
def get_comments(page_num, page_size):
    try:
        # Get a list of comments from the comments collection with pagination
        skip = (page_num - 1) * page_size
        comments_cursor = comments_collection.find().skip(skip).limit(page_size)
        comments = list(comments_cursor)
        return comments, True
    except Exception as e:
        return [], False

# Retrieve a comment by comment ID
def get_comment_by_id(comment_id):
    try:
        # Find a comment in the comments collection by its comment ID
        comment = comments_collection.find_one({'comment_id': comment_id})
        if comment:
            return comment, True
        return None, False
    except Exception as e:
        return None, False

# Insert a new comment into the collection
def insert_comment(comment_data):
    try:
        # Add a new comment to the comments collection
        result = comments_collection.insert_one(comment_data)
        if result.inserted_id:
            return str(result.inserted_id), True
        return None, False
    except Exception as e:
        return None, False
    

# Update an existing comment in the collection
def update_comment(comment_id, update_data):
    try:
        # Update the details of an existing comment in the comments collection
        result = comments_collection.update_one({'comment_id': comment_id}, {'$set': update_data})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        return False

# Delete a comment from the collection
def delete_comment(comment_id):
    try:
        # Remove a comment from the comments collection
        result = comments_collection.delete_one({'comment_id': comment_id})
        if result.deleted_count > 0:
            return True
        return False
    except Exception as e:
        return False