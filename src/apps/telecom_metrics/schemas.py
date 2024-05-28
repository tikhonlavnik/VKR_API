from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CalculateRequest(BaseModel):
    task_name: str
    samples: int = 5


class CalculateResponse(BaseModel):
    task_id: UUID
    celery_id: UUID


class CalculateResult(BaseModel):
    id: UUID
    task_id: UUID
    result_type: str
    result_value: float
    created_at: datetime
