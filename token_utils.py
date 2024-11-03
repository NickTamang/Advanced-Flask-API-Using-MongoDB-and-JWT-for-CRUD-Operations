from datetime import datetime, timezone, timedelta
from pymongo import MongoClient, ASCENDING
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
blacklist_collection = db.blacklist

# Create a TTL (Time-To-Live) index on the 'expires_at' field to automatically remove expired tokens
blacklist_collection.create_index([('expires_at', ASCENDING)], expireAfterSeconds=0)

def add_token_to_blocklist(jti, expires_in):
    # Add a token to the blacklist with an expiration time
    expiration_time = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    blacklist_collection.insert_one({'jti': jti, 'created_at': datetime.now(timezone.utc), 'expires_at': expiration_time})

def check_if_token_in_blacklist(jwt_header, jwt_payload):
    # Check if a token is in the blacklist
    jti = jwt_payload['jti']
    token_in_blacklist = blacklist_collection.find_one({'jti': jti})
    return token_in_blacklist is not None