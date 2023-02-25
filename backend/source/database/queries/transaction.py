from source.database import models, engine
from sqlalchemy.sql import text
from source.database.Database import create_session


class TransactionQuery:
    def __init__(self):
        self.transaction_model = models["transactions"]
        self.session = create_session(engine)

    def fetch_by_user_id(self, transaction_time):
        """Fetch all transaction details by transaction_time"""
        return self.session.execute(
            text(f"SELECT * FROM transactions WHERE transaction_time LIKE '{transaction_time}'")
        ).all()

    def fetch_all(self, user_id):
        """Fetch all users transactions"""
        return self.session.execute(text(f"SELECT * FROM transactions WHERE user_id LIKE '{user_id}'")).one()

    def insert(self, user_id, item_id, payment, transaction_time, delivery_time, item_price, count):
        """Add transaction to transactions table"""
        self.session.add(self.transaction_model(
            user_id=user_id,
            item_id=item_id,
            payment=payment,
            transaction_time=transaction_time,
            delivery_time=delivery_time,
            item_price=item_price,
            count=count
        ))
        self.session.commit()
        self.session.close()

    def update(self, transaction_time, new_transaction_data: dict):
        """Update transaction data in transactions table"""
        all_transaction = self.session.execute(text(f"SELECT * FROM transactions WHERE transaction_time LIKE '{transaction_time}'")).all()
        for transaction in all_transaction:
            transaction.update(new_transaction_data)
        self.session.commit()
        self.session.close()

    def delete(self, transaction_time):
        """Delete transaction by transaction_time"""
        all_transaction = self.session.execute(
            text(f"SELECT * FROM transactions WHERE transaction_time LIKE '{transaction_time}'")).all()
        for transaction in all_transaction:
            transaction.delete()

        self.session.commit()
        self.session.close()
