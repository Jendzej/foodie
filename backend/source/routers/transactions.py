import datetime

from fastapi import APIRouter, Body
from source.database.queries.transaction import TransactionQuery
from source.routers.auth import get_current_active_user
from fastapi import Depends
from source.database.models import User

router = APIRouter(
    tags=["Transactions"]
)

transaction = TransactionQuery()

example_Transaction = Body(example={
    "payment": "payment",
    "delivery_time": "2023-03-12 8:16",
    "items": [{
        "item_id": 1,
        "quantity": 4
    }]
})


@router.get("/{transaction_id}")
async def fetch_single_transaction_by_id(transaction_id: int):
    return transaction.fetch_single_transaction_details(transaction_id)


@router.get("/all/")
async def fetch_all_users_transactions(current_user: User = Depends(get_current_active_user)):
    return transaction.fetch_all(current_user.id)


@router.post("/")
async def add_transaction(body: dict = example_Transaction, current_user: User = Depends(get_current_active_user)):
    payment, delivery_time, items = body.values()
    transaction_time = datetime.datetime.now()
    delivery_time = datetime.datetime.strptime(delivery_time, '%Y-%m-%d %H:%M')
    for single_item in items:
        transaction.insert(current_user.id, single_item["item_id"], payment,
                           transaction_time, delivery_time, single_item["quantity"])
