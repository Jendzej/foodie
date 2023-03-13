from source.database import models, engine
from sqlalchemy.sql import text
from source.database.Database import create_session


class TransactionQuery:
    def __init__(self):
        self.transaction_model = models["transactions"]
        self.item_model = models["items"]
        self.transaction_details_model = models["transactions_details"]
        self.session = create_session(engine)

    def fetch_single_transaction_details(self, transaction_id):
        """Fetch all transaction details by transaction_id"""
        transaction = self.session.query(self.transaction_model).filter(
            self.transaction_model.id == transaction_id
        ).one()
        transaction_details = self.session.query(self.transaction_details_model).filter(
            self.transaction_details_model.transaction_id == transaction_id
        ).all()
        return {
            "general": transaction,
            "details": transaction_details
        }

    def fetch_all(self, user_id):
        """Fetch all users transactions"""
        # TODO: Test whether it works or not
        all_transactions = {}
        transactions = self.session.query(self.transaction_model).filter(
            self.transaction_model.user_id == user_id
        ).all()
        for single_transaction in transactions:
            all_transactions.update({
                single_transaction.id: {
                    "general": single_transaction,
                    "details": self.session.query(self.transaction_details_model).filter(
                        self.transaction_details_model.transaction_id == single_transaction.id
                    ).all()
                }
            })
        return all_transactions

    def insert(self, user_id, item_id, payment, transaction_time, delivery_time, quantity):
        """Add transaction to transactions table"""
        self.session.add(self.transaction_model(
            user_id=user_id,
            payment=payment,
            transaction_time=transaction_time,
            delivery_time=delivery_time
        ))
        self.session.commit()
        transaction_id = self.session.query(self.transaction_model)\
            .order_by(self.transaction_model.id.desc()).first().id
        item_price = self.session.query(self.item_model).filter(self.item_model.id == item_id).one().item_price
        self.session.add(self.transaction_details_model(
            transaction_id=transaction_id,
            item_id=item_id,
            quantity=quantity,
            item_price=item_price
        ))
        self.session.commit()
        self.session.close()

    def update(self, transaction_id: int, new_transaction_data: dict):
        """Update transaction with id 'transaction_id' with 'new_transaction_data' dictionary"""
        transaction_to_update = self.session.query(self.transaction_model).filter(
            self.transaction_model.id == transaction_id).one()
        transaction_to_update.update(new_transaction_data)
        self.session.commit()
        self.session.close()

    def delete(self, transaction_id):
        transaction_to_delete = self.session.query(self.transaction_model).filter(
            self.transaction_model.id == transaction_id).one()
        self.session.delete(transaction_to_delete)
        self.session.commit()
        self.session.close()
