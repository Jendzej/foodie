from sqlalchemy import Sequence, Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel


def models(engine, base):
    """Creating database models"""
    user_id_sequence = Sequence('user_id_sequence')
    item_id_sequence = Sequence('item_id_sequence')
    transaction_id_sequence = Sequence('transaction_id_sequence')
    transaction_details_sequence = Sequence('transaction_details_sequence')

    class Roles(base):
        """Roles table"""
        __tablename__ = "roles"
        role = Column(String(15), primary_key=True)
        read = Column(Boolean, default=True)
        add = Column(Boolean, default=False)
        delete = Column(Boolean, default=False)
        update = Column(Boolean, default=False)
        only_owned = Column(Boolean, default=True)

        def __repr__(self):
            """Creating columns in table"""
            return f"<Roles(role={self.role}, read={self.read}, add={self.add}, delete={self.delete}, " \
                   f"update={self.update}, only_owned={self.only_owned})>"

    class Users(base):
        """Users table"""
        __tablename__ = "users"
        id = Column(Integer, user_id_sequence, primary_key=True,
                    server_default=user_id_sequence.next_value(), unique=True)
        username = Column(String(20), unique=True)
        email = Column(String(70), unique=True)
        first_name = Column(String(30))
        last_name = Column(String(30))
        password = Column(String(150))
        role = Column(String, ForeignKey('roles.role', onupdate='CASCADE', ondelete='CASCADE'))
        transaction_item = relationship('Items', secondary='transactions', backref='transaction_items')

        def __repr__(self):
            """Creating columns in table"""
            return f"<Users(id={self.id}, username={self.username}, email={self.email}, " \
                   f"first_name={self.first_name}, last_name={self.last_name}, " \
                   f"password={self.password}, role={self.role})>"

    class Items(base):
        """Items table"""
        __tablename__ = "items"
        id = Column(Integer, item_id_sequence, primary_key=True, server_default=item_id_sequence.next_value())
        item_name = Column(String(40), unique=True)
        item_price = Column(Float)
        item_description = Column(String(300))
        item_image_url = Column(String)

        def __repr__(self):
            """Creating columns in table"""
            return f"<Items(id={self.id}, item_name={self.item_name}, " \
                   f"item_price={self.item_price}, item_description={self.item_description}, " \
                   f"item_image_url={self.item_image_url})>"

    class Transactions(base):
        """Transactions table"""
        __tablename__ = "transactions"
        id = Column(Integer, transaction_id_sequence, primary_key=True,
                    server_default=transaction_id_sequence.next_value())
        user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))
        payment = Column(String(40))
        transaction_time = Column(DateTime, default=datetime.now())
        delivery_time = Column(DateTime, default=datetime.now())

        def __repr__(self):
            return f"<Transactions(id={self.id}, user_id={self.user_id}, payment={self.payment}" \
                   f"transaction_time={self.transaction_time}, delivery_time={self.delivery_time})>"

    class TransactionsDetails(base):
        """Transactions table"""
        __tablename__ = "transactions_details"
        id = Column(Integer, transaction_id_sequence, primary_key=True,
                    server_default=transaction_details_sequence.next_value())
        transaction_id = Column(Integer, ForeignKey('transactions.id', ondelete='CASCADE', onupdate='CASCADE'))
        item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE', onupdate='CASCADE'))
        quantity = Column(Integer)
        item_price = Column(Float)

        def __repr__(self):
            return f"<TransactionsDetails(transaction_id={self.transaction_id}, item_id={self.item_id}, " \
                   f"quantity={self.quantity}, item_price={self.item_price})>"

    base.metadata.create_all(engine)
    return {
        "users": Users,
        "roles": Roles,
        "items": Items,
        "transactions": Transactions,
        "transactions_details": TransactionsDetails
    }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    mail: str
    role: str
