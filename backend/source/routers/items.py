from fastapi import APIRouter, Body, HTTPException, status, Depends
from source.database.queries.item import ItemQuery
from source.database.queries.role import RoleQuery
from source.routers.auth import get_current_active_user, User
from sqlalchemy.exc import NoResultFound, IntegrityError
router = APIRouter(
    tags=["items"]
)

item = ItemQuery()
role = RoleQuery()

example_Item = Body(example={
    "item_name": "item_name",
    "item_price": 10.99,
    "item_description": "item_description",
    "item_image_url": "www.url-image .com"
})


@router.on_event("startup")
async def startup():
    item.initial_data()


@router.get("/{item_id}")
async def fetch_by_id(item_id: int):
    try:
        return item.fetch_by_id(item_id)
    except Exception as er:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=er,
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.get("/name/{item_name}")
async def fetch_by_name(item_name: str):
    try:
        return item.fetch_by_name(item_name)
    except NoResultFound:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No row was found for phrase '{item_name}'",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as er:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=er,
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.get("/")
async def fetch_all():
    try:
        return item.fetch_all()
    except Exception as er:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=er,
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/")
async def insert(item_data: dict = example_Item, current_user: User = Depends(get_current_active_user)):
    if role.fetch(current_user.role).add:
        try:
            item_name, item_price, item_description, item_image_url = item_data.values()
            item.insert(item_name, item_price, item_description, item_image_url)
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Successfully added new item do database.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except ValueError:
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Item form is invalid. Some of data is missing.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except IntegrityError:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this name is already in database.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no permission to do that.",
            headers={"WWW-Authenticate": "Bearer"}
        )
