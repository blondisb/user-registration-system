from celery import Celery
from worker.tasks import email_tasks, report_tasks

celery_app = Celery('user_tasks')
celery_app.config_from_object('worker.celery_config')