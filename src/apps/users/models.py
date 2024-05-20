# from uuid import UUID
import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, DateTime, Boolean

from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4())
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    sex = Column(String(6), nullable=False)
    birthday = Column(DateTime(), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now())
    updated_at = Column(DateTime(), nullable=False, default=datetime.now())
    is_admin = Column(Boolean(), default=False)
