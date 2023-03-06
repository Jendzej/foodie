from fastapi import APIRouter
from source.database.queries.item import ItemQuery

router = APIRouter(
    tags=["items"]
)

item = ItemQuery()


@router.on_event("startup")
async def startup():
    item.initial_data()


@router.get("/{item_id}")
async def fetch_by_id(item_id: int):
    return item.fetch_by_id(item_id)


@router.get("/name/{item_name}")
async def fetch_by_name(item_name: str):
    return item.fetch_by_name(item_name)


@router.get("/")
async def fetch_all():
    return item.fetch_all()


@router.post("/")
async def insert(item_data: dict):
    item_name, item_price, item_description, item_image_url = item_data.values()
    item.insert(item_name, item_price, item_description, item_image_url)
