from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from source.database.queries.role import RoleQuery
from source.routers.items import router as items_router
from source.routers.auth import router as auth_router
from source.routers.users import router as users_router
from source.routers.roles import router as roles_router
from source.database import database

role = RoleQuery()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.get("/drop_db")
async def drop_database():
    database.drop_data()


app.include_router(items_router, prefix="/item")
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/user")
app.include_router(roles_router, prefix="/role")
if __name__ == "__main__":
    role.initial_data()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
