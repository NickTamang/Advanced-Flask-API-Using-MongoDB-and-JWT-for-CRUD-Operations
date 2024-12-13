import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from a .env file
load_dotenv()

class Config:
    # Secret key for JWT authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # MongoDB connection URI
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Access token expiration time (short-lived)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=220)
    
    # Refresh token expiration time (long-lived)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Google OAuth 2.0 client ID
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')