# from tasks import calculate_latency, calculate_packet_loss
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# from models import TaskInfo
from datetime import datetime
import uuid

from src.apps.telecom_metrics.models import TaskInfo
from src.celery.telecom_tasks.tasks import calculate_latency, calculate_packet_loss
from src.database import async_session


class TelecomService:
    def __init__(self):
        self.tasks = {
            "latency": calculate_latency,
            "packet_loss": calculate_packet_loss,
        }

    async def record_task_info(self, user_id, task_id, task_name, task_type):
        async with async_session() as session:
            async with session.begin():
                task_info = TaskInfo(
                    user_id=user_id,
                    task_id=task_id,
                    task_name=task_name,
                    task_type=task_type,
                    created_at=datetime.utcnow(),
                )
                session.add(task_info)
                await session.commit()

    async def calculate_latency(self, user_id, task_name, samples):
        task_id = str(uuid.uuid4())
        await self.record_task_info(user_id, task_id, task_name, "latency")
        result = self.tasks["latency"].delay(user_id, samples, task_id)
        return {"task_id": task_id, "celery_id": result.id}

    async def calculate_packet_loss(self, user_id, task_name, samples):
        task_id = str(uuid.uuid4())
        await self.record_task_info(user_id, task_id, task_name, "packet_loss")
        result = self.tasks["packet_loss"].delay(user_id, samples, task_id)
        return {"task_id": task_id, "celery_id": result.id}

    async def get_result(self, task_id):
        result = calculate_latency.AsyncResult(task_id)
        return result.result
