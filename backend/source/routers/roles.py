from fastapi import APIRouter
from source.database.queries.role import RoleQuery
from source.database.queries.user import UserQuery
import os
from dotenv import load_dotenv
from jose import jwt
load_dotenv()
router = APIRouter( 
    tags=["roles"]
)
role = RoleQuery()
user = UserQuery()


@router.on_event("startup")
async def startup():
    role.insert("user", 1, 0, 0, 0, 1)
    role.insert("admin", 1, 1, 1, 1, 0)
    user.insert(os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_FIRST_NAME"), os.getenv("ADMIN_LAST_NAME"),
                jwt.encode({os.getenv("ADMIN_USERNAME"): os.getenv("ADMIN_PASSWORD")}, os.getenv("SECRET_KEY"),
                           os.getenv("ALGORITHM", "HS256")), os.getenv("ADMIN_ROLE"))


@router.get("")
async def fetch_all():
    return role.fetch_all()
