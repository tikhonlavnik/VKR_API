import uvicorn
from fastapi import FastAPI

from src.routers.users import users_views

app = FastAPI()

app.include_router(users_views.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
