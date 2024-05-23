import uvicorn
from fastapi import FastAPI

from src.admin.users import admin_users_views
from src.routers.authorization import auth_views
from src.routers.users import users_views

app = FastAPI()

# common
app.include_router(users_views.router)
app.include_router(auth_views.router)

# admin
app.include_router(admin_users_views.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
