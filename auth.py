from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db_session

# Chave da API
API_KEY = 'j2w9UHvP4bQz9g9V7vQ4tM6z2eK5tYx3'

def validate_api_key(api_key):
    return api_key == API_KEY

def authenticate_user(email, password):
    user = db_session.query(User).filter_by(email=email).first()
    if user and user.verify_password(password):
        return True
    return False
