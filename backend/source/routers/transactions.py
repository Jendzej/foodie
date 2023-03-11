from fastapi import APIRouter, Body
from source.database.queries.transaction import TransactionQuery

router = APIRouter(
    tags=["Transactions"]
)

transaction = TransactionQuery()

example_Transaction = Body(example={
    "item_name": "item_name",
    "item_price": 10.99,
    "item_description": "item_description",
    "item_image_url": "www.url-image .com"
})


@router.get("/{item_id}")
async def fetch_single_transaction_by_time(item_id: int):
    return transaction.fetch_all()

