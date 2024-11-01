import os
import json
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash
import random

def generate_dummy_users(num_users=20):
    # Generate a list of dummy users
    users = []
    for i in range(1, num_users + 1):
        user = {
            "user_id": str(ObjectId()),
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password": generate_password_hash(f"password{i}"),
            "profile_picture": f"https://example.com/profile{i}.jpg",
            "postcode": f"AB{i} 1CD",
            "phone_number": f"23456789{i}"
        }
        users.append(user)
    return users

def generate_dummy_items(users, num_items=20):
    # Generate a list of dummy items
    items = []
    for i in range(1, num_items + 1):
        item = {
            "item_id": str(ObjectId()),
            "user_id": random.choice(users)["user_id"],
            "item_name": f"Item {i}",
            "description": f"Description for item {i}",
            "photo_url": f"https://example.com/item{i}.jpg",
            "status": random.choice(["available", "taken"])
        }
        items.append(item)
    return items

def generate_dummy_comments(users, items, num_comments=50):
    # Generate a list of dummy comments
    comments = []
    for i in range(1, num_comments + 1):
        comment = {
            "comment_id": str(ObjectId()),
            "item_id": random.choice(items)["item_id"],
            "user_id": random.choice(users)["user_id"],
            "comment_text": f"Comment text {i}",
            "timestamp": datetime.now().isoformat(),
            "reply": None
        }
        comments.append(comment)
    return comments

def save_to_json(data, filename):
    # Save data to a JSON file
    with open(filename, "w") as fout:
        json.dump(data, fout, indent=4)

if __name__ == "__main__":
    # Create directory if it doesn't exist
    os.makedirs("/Users/nicktamang/UniversityY3/Full-stack/CW1/CW1draft1/datasetcw1_json", exist_ok=True)

    # Generate dummy data
    users = generate_dummy_users()
    items = generate_dummy_items(users)
    comments = generate_dummy_comments(users, items)

    # Save dummy data to JSON files
    save_to_json(users, "/Users/nicktamang/UniversityY3/Full-stack/CW1/CW1draft1/datasetcw1_json/users.json")
    save_to_json(items, "/Users/nicktamang/UniversityY3/Full-stack/CW1/CW1draft1/datasetcw1_json/items.json")
    save_to_json(comments, "/Users/nicktamang/UniversityY3/Full-stack/CW1/CW1draft1/datasetcw1_json/comments.json")