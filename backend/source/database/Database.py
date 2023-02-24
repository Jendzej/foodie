import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from models import models
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import time
load_dotenv()


class Database:
    """Database class"""

    def __init__(self):
        self.database_url = URL.create(
            "postgresql",
            username=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASS"),
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DATABASE")
        )
        self.engine = create_engine(self.database_url)
        self.base = declarative_base()
        self.models = models(self.engine, self.base)

    def connect(self, tries=5):
        """Connecting to database"""
        count = 0
        while count < tries:
            try:
                self.engine.connect()
                print("Connected!")
                return
            except OperationalError:
                time.sleep(2)
                print(f"Trying again... ({count} out of {tries} tries)")


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()
