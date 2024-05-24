from celery import Celery

from config import Config


# Убедитесь, что переменные окружения загружены
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery("my_project", broker=Config.REDIS_URL, backend=Config.REDIS_URL)

# Автоматически обнаруживать задачи в модуле `telecom_tasks`
celery_app.autodiscover_tasks(["src.celery.telecom_tasks"])
#
#
# def make_celery():
#     celery = Celery(
#         "telecom_metrics", backend=Config.REDIS_URL, broker=Config.REDIS_URL
#     )
#     celery.conf.update(
#         result_expires=3600,
#     )
#     return celery
#
#
# celery_app = make_celery()
