from pymongo import MongoClient
from config import Config
import re

# Initializing MongoDB client and database
client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()

# Collections
users_collection = db.Users

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
        print(f"Error occurred: {e}")
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
        print(f"Error occurred: {e}")
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
        print(f"Error occurred: {e}")
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
        print(f"Error occurred: {e}")
        return False

# Retrieve a paginated list of items
def get_items(page_num, page_size):
    try:
        # Get all users
        users_cursor = users_collection.find()
        all_items = []
        
        # Collect all items from all users
        for user in users_cursor:
            for item in user.get('items', []):
                item['_id'] = str(user['_id'])  # Include the user's _id in the item data
                all_items.append(item)
        
        # Apply pagination to the items list
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        paginated_items = all_items[start_index:end_index]
        
        return paginated_items, True
    except Exception as e:
        print(f"Error occurred: {e}")
        return [], False


def get_item_by_id(item_id):
    try:
        # Find an item in the users collection by its item ID and include _id
        user = users_collection.find_one(
            {'items.item_id': item_id}, 
            {'items.$': 1, '_id': 1}  # Include _id explicitly
        )
        if user and 'items' in user:
            item = user['items'][0]
            item['_id'] = str(user['_id'])  # Include the user's _id in the item data if needed
            return item, True
        return None, False
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, False


# Retrieve items by partial name match
def get_items_by_partial_name(item_name_prefix):
    try:
        # Use regex to match the item name prefix
        regex = re.compile(f'^{item_name_prefix}', re.IGNORECASE)
        items = []
        
        # Modify the query to include all matching items and the document's _id
        users_cursor = users_collection.find(
            {'items.item_name': regex}, 
            {'items': 1, '_id': 1}  # Include the entire items array and the _id of the document
        )
        
        for user in users_cursor:
            for item in user.get('items', []):
                # Add the user's _id to each item (so you can identify which user the item belongs to)
                item['_id'] = str(user['_id'])  # Add the user's _id to the item
                items.append(item)  # Append the item to the list
        
        return items, True
    except Exception as e:
        print(f"Error occurred: {e}")
        return [], False
    

# Insert a new item into the collection
def insert_item(user_id, item_data):
    try:
        # Add a new item to the user's items in the users collection
        result = users_collection.update_one({'user_id': user_id}, {'$push': {'items': item_data}})
        if result.modified_count > 0:
            return item_data['item_id'], True
        return None, False
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, False

# Update an existing item in the collection
def update_item(item_id, update_data):
    try:
        # Update the details of an existing item in the users collection
        result = users_collection.update_one({'items.item_id': item_id}, {'$set': {'items.$': update_data}})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# Delete an item from the collection
def delete_item(item_id):
    try:
        # Remove an item from the users collection
        result = users_collection.update_one({'items.item_id': item_id}, {'$pull': {'items': {'item_id': item_id}}})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# Retrieve a paginated list of comments
def get_comments(page_num, page_size):
    try:
        # Get a list of comments from the users collection with pagination
        comments = []
        skip = (page_num - 1) * page_size
        users_cursor = users_collection.find().skip(skip).limit(page_size)
        for user in users_cursor:
            for item in user.get('items', []):
                comments.extend(item.get('comments', []))
        return comments, True
    except Exception as e:
        print(f"Error occurred: {e}")
        return [], False
    

# Retrieve a comment by comment ID
def get_comment_by_id(comment_id):
    try:
        # Find a comment in the users collection by its comment ID and include _id
        user = users_collection.find_one(
            {'items.comments.comment_id': comment_id}, 
            {'items.comments.$': 1, '_id': 1}  # Include _id explicitly
        )
        if user and 'items' in user:
            for item in user['items']:
                if 'comments' in item:
                    for comment in item['comments']:
                        if comment['comment_id'] == comment_id:
                            comment['_id'] = str(user['_id'])  # Include the user's _id in the comment data if needed
                            return comment, True
        return None, False
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, False
    
# Retrieve comments by item ID
def get_comments_by_item_id(item_id):
    try:
        # Find comments in the users collection by item ID and include _id
        user = users_collection.find_one(
            {'items.item_id': item_id}, 
            {'items.$': 1, '_id': 1}  # Include _id explicitly
        )
        if user and 'items' in user:
            item = user['items'][0]
            comments = item.get('comments', [])
            for comment in comments:
                comment['_id'] = str(user['_id'])  # Include the user's _id in the comment data if needed
            return comments, True
        return None, False
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, False

#done Insert a new comment into the collection
def insert_comment(comment_data):
    try:
        item_id = comment_data['item_id']
        # Add a new comment to the item's comments in the users collection
        result = users_collection.update_one(
            {'items.item_id': item_id}, 
            {'$push': {'items.$.comments': comment_data}}
        )
        if result.modified_count > 0:
            return comment_data['comment_id'], True
        return None, False
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, False

#done Update an existing comment in the collection
def update_comment(comment_id, update_data):
    try:
        # Update the details of an existing comment in the users collection
        result = users_collection.update_one(
            {'items.comments.comment_id': comment_id}, 
            {'$set': {'items.$[item].comments.$[comment].reply': update_data['reply']}},
            array_filters=[{'item.comments.comment_id': comment_id}, {'comment.comment_id': comment_id}]
        )
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# Delete a comment from the collection
def delete_comment(comment_id):
    try:
        # Remove a comment from the users collection
        result = users_collection.update_one({'items.comments.comment_id': comment_id}, {'$pull': {'items.$.comments': {'comment_id': comment_id}}})
        if result.modified_count > 0:
            return True
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False