

@celery_app.task(base=CallbackTask, bind=True)
def generate_profile_report(self, user_id: str, task_id: str):
    """Genera informe de perfil con procesamiento optimizado"""
    try:
        # Verificar idempotencia
        if check_task_already_completed(task_id):
            logger.info(f"Task {task_id} already completed, skipping")
            return {"status": "already_completed", "task_id": task_id}
        
        # Marcar como en progreso
        update_task_status(task_id, 'in_progress')
        
        # Obtener datos del usuario
        user_data = get_user_data(user_id)
        
        # Generar estadísticas del perfil
        profile_stats = {
            "user_id": user_id,
            "registration_date": user_data.created_at.isoformat(),
            "profile_completeness": calculate_profile_completeness(user_data),
            "recommendations": generate_recommendations(user_data),
            "generated_at": datetime.now().isoformat()
        }
        
        # Generar PDF (opcional)
        pdf_path = None
        if user_data.metadata.get('generate_pdf', False):
            pdf_path = generate_pdf_report(user_id, profile_stats)
        
        # Guardar resultado
        result = {
            "status": "generated",
            "stats": profile_stats,
            "pdf_path": pdf_path,
            "task_id": task_id
        }
        
        save_task_result(user_id, task_id, 'generate_profile_report', result)
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating report for task {task_id}: {e}")
        raise self.retry(exc=e, countdown=120, max_retries=5)
