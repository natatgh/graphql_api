import secrets
from models import APIToken
from database import db_session

def generate_api_token(user_id):
    token = secrets.token_hex(32)
    api_token = APIToken(token=token, user_id=user_id)
    db_session.add(api_token)
    db_session.commit()
    return token

def validate_api_token(token):
    api_token = APIToken.query.filter_by(token=token).first()
    return api_token is not None
