# celery_config.py
from kombu import Queue

# Configuración de colas con prioridades
CELERY_TASK_ROUTES = {
    'user_tasks.send_welcome_email': {'queue': 'high_priority'},
    'user_tasks.generate_profile_report': {'queue': 'low_priority'},
}

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = (
    Queue('high_priority', routing_key='high_priority'),
    Queue('low_priority', routing_key='low_priority'),
    Queue('default', routing_key='default'),
)

# Configuración de workers
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

