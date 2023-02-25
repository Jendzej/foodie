from source.database import models, engine
from sqlalchemy.sql import text
from source.database.Database import create_session


class ItemQuery:
    def __init__(self):
        self.item_model = models["items"]
        self.session = create_session(engine)

    def fetch_by_name(self, item_name):
        """Fetch item details by item_name"""
        return self.session.execute(text(f"SELECT * FROM items WHERE item_name LIKE '{item_name}'")).one()

    def fetch_by_id(self, item_id):
        """Fetch item details by item_id"""
        return self.session.execute(text(f"SELECT * FROM items WHERE id LIKE '{item_id}'")).all()

    def fetch_all(self):
        """Fetch all items data"""
        return self.session.execute(text("SELECT * FROM items")).all()

    def insert(self, item_name: str, item_price: float, item_description: str, item_image_url: str):
        """Add item to items table"""
        self.session.add(self.item_model(
            item_name=item_name,
            item_price=item_price,
            item_description=item_description,
            item_image_url=item_image_url
        ))
        self.session.commit()
        self.session.close()

    def initial_data(self):
        """Create some items on start-up"""
        print("Adding some", self.session)
        # TODO: end this shit

    def update(self, item_id, new_item_data: dict):
        """Update item data in items table"""
        self.session.query(self.item_model).filter(self.item_model.id == item_id).update(new_item_data)

    def delete(self, item_id):
        """Delete item by id"""
        self.session.query(self.item_model).filter(self.item_model.id == item_id).delete()
        self.session.commit()
        self.session.close()
