from celery import Celery
from worker.tasks import email_tasks, report_tasks
from celery.exceptions import Retry


# Configuración de Celery con Redis como broker
celery_app = Celery(
    'user_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# celery_app = Celery('user_tasks')
celery_app.config_from_object('worker.celery_config')