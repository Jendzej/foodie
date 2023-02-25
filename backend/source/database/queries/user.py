from source.database import models, engine
from source.database.Database import create_session
from sqlalchemy.sql import text
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class UserQuery:
    def __init__(self):
        self.user_model = models["users"]
        self.session = create_session(engine)

    def fetch(self, user_id):
        """Fetch one row by user_id"""
        return self.session.execute(text(f"SELECT * FROM Users WHERE id LIKE '{user_id}'")).fetchone()

    def fetch_all(self):
        """Fetch all users data"""
        return self.session.execute(text("SELECT * FROM users")).fetchall()

    def insert(self, username, email, first_name, last_name, password, role):
        """Add data to users table"""
        self.session.add(self.user_model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role
        ))
        self.session.commit()
        self.session.close()

    def update(self, user_id, new_user_data):
        """Update user with new_user_data. If new_user_data (dict) contains username, password
        is updated too (because of JWT token, which is generating from dict {username: password})"""
        user_to_update = self.session.query(self.user_model).filter(self.user_model.id == user_id).one()
        if 'username' in new_user_data.keys():
            if 'password' in new_user_data.keys():
                new_user_data['password'] = jwt.encode(
                    {new_user_data['username']: new_user_data['password']}, SECRET_KEY, ALGORITHM)
            else:
                old_password = jwt.decode(user_to_update.password, SECRET_KEY, ALGORITHM)
                new_user_data['password'] = jwt.encode(
                    {new_user_data['username']: old_password[user_to_update.username]}, SECRET_KEY, ALGORITHM)
        else:
            if 'password' in new_user_data.keys():
                new_user_data['password'] = jwt.encode(
                    {user_to_update.username: new_user_data['password']}, SECRET_KEY, ALGORITHM)
        self.session.query(self.user_model).filter(self.user_model.id == user_id).update(new_user_data)
        self.session.commit()
        self.session.close()

    def delete(self, user_id):
        """Delete user by user_id"""
        self.session.query(self.user_model).filter(self.user_model.id == user_id).delete()
        self.session.commit()
        self.session.close()
