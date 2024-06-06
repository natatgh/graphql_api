import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Define the path for SQLite in the /tmp directory
DATABASE_PATH = "/tmp/database.db"

# Create the engine and database session
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
