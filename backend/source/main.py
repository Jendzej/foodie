from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from source.database.queries.role import RoleQuery
from source.routers.items import router as items_router

print("HALO")

role = RoleQuery()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)
app.include_router(items_router, prefix="/item")
if __name__ == "__main__":
    print("starting")
    role.initial_data()
    print(role.fetch_all())
    print(role.fetch("admin"))
    role.delete("seller")
    print(role.fetch_all())
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
