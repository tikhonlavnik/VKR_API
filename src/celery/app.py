from celery import Celery

from config import Config

from dotenv import load_dotenv


load_dotenv()

celery_app = Celery("my_project", broker=Config.REDIS_URL, backend=Config.REDIS_URL)

celery_app.autodiscover_tasks(["src.celery.telecom_tasks.tasks"])
