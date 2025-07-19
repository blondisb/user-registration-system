# monitoring.py
from celery.signals import task_prerun, task_postrun, task_failure
from prometheus_client import Counter, Histogram, Gauge

# Métricas de Prometheus
TASK_COUNTER = Counter('celery_tasks_total', 'Total tasks', ['task_name', 'status'])
TASK_DURATION = Histogram('celery_task_duration_seconds', 'Task duration', ['task_name'])
QUEUE_SIZE = Gauge('celery_queue_size', 'Queue size', ['queue_name'])

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Monitoreo antes de ejecutar tarea"""
    TASK_COUNTER.labels(task_name=task.name, status='started').inc()

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **kwds):
    """Monitoreo después de ejecutar tarea"""
    TASK_COUNTER.labels(task_name=task.name, status='completed').inc()

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Monitoreo de fallos"""
    TASK_COUNTER.labels(task_name=sender.name, status='failed').inc()