from source.database import models, engine
from source.database.Database import create_session


class RoleQuery:
    def __init__(self):
        self.role_model = models["roles"]
        self.session = create_session(engine)

    def fetch(self, role):
        """Fetch role details by role name"""
        return self.session.execute(f"SELECT * FROM Roles WHERE role LIKE {role}")

    def fetch_all(self):
        """Fetch all roles data"""
        return self.session.execute("SELECT * FROM roles").fetchall()

    def insert(self, role, read=True, add=False, delete=False, update=False, only_owned=True):
        self.session.add(self.role_model(
            role=role,
            read=read,
            add=add,
            delete=delete,
            update=update,
            only_owned=only_owned
        ))
        self.session.commit()
        self.session.close()
