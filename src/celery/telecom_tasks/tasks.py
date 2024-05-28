from datetime import datetime
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from src.apps.telecom_metrics.models import TelecomResults
from src.celery.app import celery_app

engine = create_engine(Config.CELERY_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


@celery_app.task
def calculate_latency_result(samples, task_id):
    session = Session()
    try:
        latency_sum = sum(random.uniform(10, 100) for _ in range(samples))
        result_value = latency_sum / samples

        result = TelecomResults(
            task_id=task_id,
            result_type="latency",
            result_value=result_value,
            created_at=datetime.utcnow(),
        )
        session.add(result)
        session.commit()
        return result_value
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
        return None
    finally:
        session.close()


@celery_app.task
async def calculate_packet_loss_result(samples, task_id):
    session = Session()
    try:
        packet_loss_sum = sum(random.uniform(0, 10) for _ in range(samples))
        result_value = packet_loss_sum / samples

        result = TelecomResults(
            task_id=task_id,
            result_type="packet_loss",
            result_value=result_value,
            created_at=datetime.utcnow(),
        )
        session.add(result)
        session.commit()
        return result_value
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
        return None
    finally:
        session.close()
