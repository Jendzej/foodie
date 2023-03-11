from fastapi import APIRouter, Body
from source.database.queries.user import UserQuery
import os
from dotenv import load_dotenv
from jose import jwt
load_dotenv()

router = APIRouter(
    tags=["users"]
)
user = UserQuery()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

example_User = Body(example={
    "username": "user",
    "email": "email",
    "first_name": "First",
    "last_name": "Last",
    "password": "password",
    "role": "user"
})


@router.get("/{user_id}")
async def fetch_by_id(user_id: int):
    """Fetch user data by id"""
    return user.fetch(user_id)


@router.get("/username/{username}")
async def fetch_by_username(username: str):
    """Fetch user data by username"""
    return user.fetch_by_username(username)


@router.get("/all/")
async def fetch_all():
    """Fetch all users data"""
    return user.fetch_all()


@router.post("/")
async def add_user(user_data: dict = example_User):
    username, email, first_name, last_name, password, role = user_data.values()
    user.insert(username, email, first_name, last_name, jwt.encode({username: password}, SECRET_KEY, ALGORITHM), role)

