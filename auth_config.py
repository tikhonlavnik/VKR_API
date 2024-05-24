from pydantic_settings import BaseSettings
from config import Config


class Settings(BaseSettings):
    secret_key: str = Config.SECRET_KEY
    algorithm: str = Config.ALGORITHM
    access_token_expire_minutes: int = Config.ACCESS_TOKEN_EXPIRE_MINUTES

    class Config:
        env_file = ".env"


settings = Settings
