from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config
from routes import auth_bp, users_bp, items_bp, comments_bp
from token_utils import check_if_token_in_blacklist

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

client = MongoClient(app.config['MONGO_URI'])
db = client.get_default_database()
blacklist_collection = db.blacklist

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return check_if_token_in_blacklist(jwt_header, jwt_payload)

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(items_bp)
app.register_blueprint(comments_bp)

if __name__ == "__main__":
    app.run(debug=True)