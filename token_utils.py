from datetime import datetime, timezone, timedelta
from pymongo import MongoClient, ASCENDING
from config import Config
from flask_jwt_extended import decode_token

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
blacklist_collection = db.blacklist

# Ensure an index on the 'expires_at' field to support TTL (Time-To-Live) index
blacklist_collection.create_index([('expires_at', ASCENDING)], expireAfterSeconds=0)  # TTL index

def add_token_to_blocklist(jti, expires_in):
    expiration_time = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    blacklist_collection.insert_one({'jti': jti, 'created_at': datetime.now(timezone.utc), 'expires_at': expiration_time})

def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token_in_blacklist = blacklist_collection.find_one({'jti': jti})
    return token_in_blacklist is not None