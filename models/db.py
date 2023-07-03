from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import get_settings

settings = get_settings()

engine = create_engine(settings.sqlalchemy_database_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

