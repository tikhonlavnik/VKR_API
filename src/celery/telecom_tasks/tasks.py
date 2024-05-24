from datetime import datetime
import random

from src.apps.telecom_metrics.models import TelecomResults
from src.celery.app import celery_app
from src.database import async_session


@celery_app.task
async def calculate_latency(user_id, samples, task_id):
    latency_sum = sum(random.uniform(10, 100) for _ in range(samples))
    result_value = latency_sum / samples

    async with async_session() as session:
        async with session.begin():
            result = TelecomResults(
                user_id=user_id,
                task_id=task_id,
                result_type="latency",
                result_value=result_value,
                created_at=datetime.utcnow(),
            )
            session.add(result)
            await session.commit()
    return result_value


@celery_app.task
async def calculate_packet_loss(user_id, samples, task_id):
    packet_loss_sum = sum(random.uniform(0, 10) for _ in range(samples))
    result_value = packet_loss_sum / samples

    async with async_session() as session:
        async with session.begin():
            result = TelecomResults(
                user_id=user_id,
                task_id=task_id,
                result_type="packet_loss",
                result_value=result_value,
                created_at=datetime.utcnow(),
            )
            session.add(result)
            await session.commit()
    return result_value
