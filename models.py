from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    contracts = relationship('Contract', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)
    fidelity = Column(Integer)
    amount = Column(Float)
    user = relationship('User', back_populates='contracts')

class APIToken(Base):
    __tablename__ = 'api_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
