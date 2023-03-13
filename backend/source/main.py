from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from source.database.models import User
from source.database.queries.role import RoleQuery
from source.routers.items import router as items_router
from source.routers.auth import router as auth_router, get_current_active_user
from source.routers.users import router as users_router
from source.routers.roles import router as roles_router
from source.routers.transactions import router as transactions_router
from source.database import database

role = RoleQuery()
app = FastAPI(
    title="FoodieAPI",
    description="API for best e-commerce shop"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.get("/drop_database", tags=["Administration"])
async def drop_database(current_user: User = Depends(get_current_active_user)):
    if current_user.role == "admin":
        try:
            database.drop_data()
            database.drop_sequences()
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Database and sequences successfully dropped!",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception as er:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=er,
                headers={"WWW-Authenticate": "Bearer"}
            )
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no permission to do that.",
            headers={"WWW-Authenticate": "Bearer"}
        )


app.include_router(items_router, prefix="/item")
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/user")
app.include_router(roles_router, prefix="/role")
app.include_router(transactions_router, prefix="/transaction")

if __name__ == "__main__":
    role.initial_data()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
