import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CallbackTask(Task):
    """Clase base para tareas con callbacks automáticos"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Callback ejecutado cuando la tarea es exitosa"""
        update_task_status(task_id, 'completed', result=retval)
        logger.info(f"Task {task_id} completed successfully")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Callback ejecutado cuando la tarea falla"""
        update_task_status(task_id, 'failed', error=str(exc))
        logger.error(f"Task {task_id} failed: {exc}")
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Callback ejecutado en reintentos"""
        update_task_status(task_id, 'retrying', error=str(exc))
        logger.warning(f"Task {task_id} retrying: {exc}")
