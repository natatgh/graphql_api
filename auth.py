import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db_session

SECRET_KEY = 'j2w9UHvP4bQz9g9V7vQ4tM6z2eK5tYx3'  # Coloque a chave secreta gerada aqui
API_KEY = 'j2w9UHvP4bQz9g9V7vQ4tM6z2eK5tYx3'  # Chave da API

def generate_api_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def validate_api_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def authenticate_user(email, password):
    user = db_session.query(User).filter_by(email=email).first()
    if user and user.verify_password(password):
        return generate_api_token(user.id)
    return None

def validate_api_key(api_key):
    return api_key == API_KEY
