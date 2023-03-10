from fastapi import APIRouter
from source.database.queries.role import RoleQuery

router = APIRouter(
    tags=["roles"]
)
role = RoleQuery()


@router.on_event("startup")
async def startup():
    role.insert("user", 1, 0, 0, 0, 1)
    role.insert("admin", 1, 1, 1, 1, 0)


@router.get("")
async def fetch_all():
    return role.fetch_all()
