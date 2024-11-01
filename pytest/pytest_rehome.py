import sys
import os
import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

# Add the parent directory to the system path to import the app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from models.some_utility import insert_user, insert_item, insert_comment

# Fixture to provide the Flask app instance
@pytest.fixture
def app():
    yield flask_app

# Fixture to provide a test client for the Flask app
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture to provide an access token for authentication
@pytest.fixture
def access_token(app):
    with app.app_context():
        # Create a test user and generate an access token for them
        user_data = {
            "user_id": "131313131313131313131313",
            "username": "Nick Tester",
            "email": "pytest1313131331@gmail.com",
            "password": generate_password_hash("NickTester123"),  # Hash the password
            "profile_picture": "http://example.com/profile.jpg",
            "postcode": "12345",
            "phone_number": "123-456-7890"
        }
        insert_user(user_data)
        return create_access_token(identity="131313131313131313131313")

# Test case for user registration
def test_register_user(client):
    response = client.post("/api/rehome/users", json={
        "username": "Nick Tester",
        "email": "pytest1313131331@gmail.com",
        "password": "NickTester123",
        "profile_picture": "http://example.com/profile.jpg",
        "postcode": "12345",
        "phone_number": "123-456-7890"
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'

# Test case for user login
def test_login(client):
    response = client.post("/api/rehome/login", json={
        "email": "pytest1313131331@gmail.com",
        "password": "NickTester123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

# Test case for fetching a list of users
def test_get_users(client, access_token):
    response = client.get("/api/rehome/users", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test case for updating a user
def test_update_user(client, access_token):
    response = client.put("/api/rehome/users/131313131313131313131313", json={
        "username": "Updated Nick Tester",
        "email": "updatednicktester@gmail.com",
        "profile_picture": "http://example.com/updated_profile.jpg",
        "postcode": "54321",
        "phone_number": "098-765-4321"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

# Test case for deleting a user
def test_delete_user(client, access_token):
    response = client.delete("/api/rehome/users/131313131313131313131313", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

# Test case for sharing a new item
def test_share_item(client, access_token):
    response = client.post("/api/rehome/items", json={
        "item_name": "Item 1",
        "description": "Description for item 1",
        "photo_url": "http://example.com/item1.jpg",
        "status": "available"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'

# Test case for fetching a list of items
def test_get_items(client, access_token):
    response = client.get("/api/rehome/items", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test case for fetching an item by its ID
def test_get_item_by_id(client, access_token):
    item_id = "test_item_id"
    insert_item({
        "item_id": item_id,
        "user_id": "131313131313131313131313",
        "item_name": "Item 1",
        "description": "Description for item 1",
        "photo_url": "http://example.com/item1.jpg",
        "status": "available"
    })
    response = client.get(f"/api/rehome/items/{item_id}", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['item_id'] == item_id

# Test case for fetching items by name
def test_get_items_by_name(client, access_token):
    response = client.get("/api/rehome/items/name/Item", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test case for updating the status of an item
def test_update_item_status(client, access_token):
    item_id = "test_item_id"
    insert_item({
        "item_id": item_id,
        "user_id": "131313131313131313131313",
        "item_name": "Item 1",
        "description": "Description for item 1",
        "photo_url": "http://example.com/item1.jpg",
        "status": "available"
    })
    response = client.patch(f"/api/rehome/items/{item_id}", json={
        "status": "taken"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

# Test case for deleting an item
def test_delete_item(client, access_token):
    item_id = "test_item_id"
    insert_item({
        "item_id": item_id,
        "user_id": "131313131313131313131313",
        "item_name": "Item 1",
        "description": "Description for item 1",
        "photo_url": "http://example.com/item1.jpg",
        "status": "available"
    })
    response = client.delete(f"/api/rehome/items/{item_id}", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

# Test case for adding a comment to an item
def test_add_comment(client, access_token):
    item_id = "test_item_id"
    insert_item({
        "item_id": item_id,
        "user_id": "131313131313131313131313",
        "item_name": "Item 1",
        "description": "Description for item 1",
        "photo_url": "http://example.com/item1.jpg",
        "status": "available"
    })
    response = client.post("/api/rehome/comments", json={
        "item_id": item_id,
        "comment_text": "This is a test comment"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'

# Test case for fetching comments
def test_get_comments(client, access_token):
    response = client.get("/api/rehome/comments", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test case for editing a comment
def test_edit_comment(client, access_token):
    comment_id = "test_comment_id"
    insert_comment({
        "comment_id": comment_id,
        "item_id": "test_item_id",
        "user_id": "131313131313131313131313",
        "comment_text": "This is a test comment",
        "timestamp": "2021-01-01T00:00:00",
        "reply": None
    })
    response = client.put(f"/api/rehome/comments/{comment_id}", json={
        "comment_text": "Updated comment text"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

# Test case for replying to a comment
def test_reply_comment(client, access_token):
    comment_id = "test_comment_id"
    insert_comment({
        "comment_id": comment_id,
        "item_id": "test_item_id",
        "user_id": "131313131313131313131313",
        "comment_text": "This is a test comment",
        "timestamp": "2021-01-01T00:00:00",
        "reply": None
    })
    response = client.post(f"/api/rehome/comments/{comment_id}/reply", json={
        "reply": "This is a test reply"
    }, headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

# Test case for deleting a comment
def test_delete_comment(client, access_token):
    comment_id = "test_comment_id"
    insert_comment({
        "comment_id": comment_id,
        "item_id": "test_item_id",
        "user_id": "131313131313131313131313",
        "comment_text": "This is a test comment",
        "timestamp": "2021-01-01T00:00:00",
        "reply": None
    })
    response = client.delete(f"/api/rehome/comments/{comment_id}", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'