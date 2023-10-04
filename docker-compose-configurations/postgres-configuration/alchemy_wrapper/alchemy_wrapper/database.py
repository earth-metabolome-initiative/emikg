"""Mofule to create a database engine for sqlalchemy"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = (
    f"postgresql://{os.environ['POSTGRES_USER']}:"
    f"{os.environ['POSTGRES_PASSWORD']}@postgres_database:5432"
    f"/{os.environ['POSTGRES_DB']}"
)

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
