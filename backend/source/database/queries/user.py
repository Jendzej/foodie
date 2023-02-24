from source.database import models, engine
from source.database.Database import create_session


class UserQuery:
    def __init__(self):
        self.user_model = models["users"]
        self.session = create_session(engine)

    def fetch(self, user_id):
        """Fetch one row by user_id"""
        return self.session.execute(f"SELECT * FROM Users WHERE id LIKE {user_id}").fetchone()

    def fetch_all(self):
        """Fetch all users data"""
        return self.session.execute("SELECT * FROM users").fetchall()

    def insert(self, username, email, first_name, last_name, password, role):
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
