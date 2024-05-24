import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship

from src.apps.users.models import Users
from src.database import Base


class TelecomResults(Base):
    __tablename__ = "telecom_results"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    task_id = Column(String, nullable=False)
    result_type = Column(String, nullable=False)  # latency or packet_loss
    result_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TaskInfo(Base):
    __tablename__ = "task_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    task_id = Column(String, nullable=False)
    task_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)  # latency or packet_loss
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users")
