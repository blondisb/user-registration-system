
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@celery_app.task(base=CallbackTask, bind=True)
def send_welcome_email(self, email: str, nombre: str, user_id: str, task_id: str):
    """Envía correo de bienvenida con manejo robusto de errores"""
    try:
        # Verificar idempotencia
        if check_task_already_completed(task_id):
            logger.info(f"Task {task_id} already completed, skipping")
            return {"status": "already_completed", "task_id": task_id}
        
        # Marcar como en progreso
        update_task_status(task_id, 'in_progress')
        
        # Lógica de envío de correo
        msg = MIMEMultipart()
        msg['From'] = "noreply@miapp.com"
        msg['To'] = email
        msg['Subject'] = f"¡Bienvenido/a {nombre}!"
        
        body = f"""
        Hola {nombre},
        
        ¡Bienvenido/a a nuestra plataforma! 
        Tu cuenta ha sido creada exitosamente.
        
        Saludos,
        El equipo de MiApp
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Envío con reintentos automáticos
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("usuario@gmail.com", "password")
        server.send_message(msg)
        server.quit()
        
        # Registrar resultado
        result = {
            "status": "sent",
            "email": email,
            "sent_at": datetime.now().isoformat(),
            "task_id": task_id
        }
        
        save_task_result(user_id, task_id, 'send_welcome_email', result)
        
        return result
        
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error in task {task_id}: {e}")
        # Reintento automático para errores de red
        raise self.retry(exc=e, countdown=60, max_retries=3)
    
    except Exception as e:
        logger.error(f"Unexpected error in task {task_id}: {e}")
        raise