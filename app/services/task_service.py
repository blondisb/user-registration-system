
# Funciones auxiliares para manejo de estado
async def update_task_status(task_id: str, status: str, result=None, error=None):
    """Actualiza el estado de una tarea en la BD"""
    # Implementación de actualización en BD
    pass

async def check_task_already_completed(task_id: str) -> bool:
    """Verifica si una tarea ya fue completada (idempotencia)"""
    # Implementación de verificación en BD
    pass

async def save_task_result(user_id: str, task_id: str, task_type: str, result: dict):
    """Guarda el resultado de una tarea"""
    # Implementación de guardado en BD
    pass