import uvicorn
from fastapi import FastAPI

from src.admin.users import admin_users_views
from src.celery.app import celery_app
from src.routers.authorization import auth_views
from src.routers.telecom_metrics import telecom_views
from src.routers.users import users_views

app = FastAPI()

# common
app.include_router(users_views.router)
app.include_router(auth_views.router)
app.include_router(telecom_views.router)

# admin
app.include_router(admin_users_views.router)


# @app.on_event("startup")
# async def startup_event():
#     # Инициализация Celery
#     celery_app.start()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
