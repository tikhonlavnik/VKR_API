from sqlalchemy import select
from datetime import datetime

import uuid

from src.apps.telecom_metrics.models import TaskInfo, TelecomResults
from src.celery.telecom_tasks.tasks import (
    calculate_latency_result,
    calculate_packet_loss_result,
)
from src.database import async_session


class TelecomService:
    def __init__(self):
        self.tasks = {
            "latency": calculate_latency_result,
            "packet_loss": calculate_packet_loss_result,
        }

    @staticmethod
    async def record_task_info(user_id, task_id, task_name, task_type):
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
        result = calculate_latency_result.delay(samples, task_id)
        return {"task_id": task_id, "celery_id": result.id}

    async def calculate_packet_loss(self, user_id, task_name, samples):
        task_id = str(uuid.uuid4())
        await self.record_task_info(user_id, task_id, task_name, "packet_loss")
        result = self.tasks["packet_loss"].delay(samples, task_id)
        return {"task_id": task_id, "celery_id": result.id}

    @staticmethod
    async def get_result(task_id):
        async with async_session() as session:
            async with session.begin():
                stmt = select(TelecomResults).where(TelecomResults.id == task_id)
                result = await session.execute(stmt)
                result_record = result.scalars().first()
        return result_record
