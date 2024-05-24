from pydantic import BaseModel


class CalculateRequest(BaseModel):
    task_name: str
    samples: int
