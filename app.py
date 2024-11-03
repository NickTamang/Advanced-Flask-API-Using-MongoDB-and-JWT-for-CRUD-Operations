from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config
from routes import auth_bp, users_bp, items_bp, comments_bp
from token_utils import check_if_token_in_blacklist

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the JWT Manager with the Flask app
jwt = JWTManager(app)

# Initialize MongoDB client and get the default database
try:
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_default_database()
    blacklist_collection = db.blacklist
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")

# Define a function to check if a token is in the blacklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return check_if_token_in_blacklist(jwt_header, jwt_payload)

# Register blueprints for different routes
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(items_bp)
app.register_blueprint(comments_bp)

# Run the Flask application
if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error running the app: {str(e)}")