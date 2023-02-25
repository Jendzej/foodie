from source.database import models, engine
from sqlalchemy.sql import text
from source.database.Database import create_session


class RoleQuery:
    def __init__(self):
        self.role_model = models["roles"]
        self.session = create_session(engine)

    def fetch(self, role):
        """Fetch role details by role name"""
        return self.session.execute(text(f"SELECT * FROM Roles WHERE role LIKE '{role}'")).fetchone()

    def fetch_all(self):
        """Fetch all roles data"""
        return self.session.execute(text("SELECT * FROM roles")).fetchall()

    def insert(self, role, read=True, add=False, delete=False, update=False, only_owned=True):
        """Add role to roles table"""
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

    def initial_data(self):
        """Create some roles on start-up"""
        self.insert("admin", True, True, True, True, False)
        self.insert("user", True, False, False, False, True)
        self.insert("seller", True, True, True, True, True)

    def update(self, role, new_role_data: dict):
        """Update role data in roles table"""
        self.session.query(self.role_model).filter(self.role_model.role == role).update(new_role_data)

    def delete(self, role):
        """Delete role by role name"""
        self.session.query(self.role_model).filter(self.role_model.role == role).delete()
        self.session.commit()
        self.session.close()
