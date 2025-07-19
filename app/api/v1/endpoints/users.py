from fastapi import FastAPI, HTTPException, status
import uuid
from celery import Celery
from pydantic import BaseModel, EmailStr

app = FastAPI()

@app.post("/api/v1/users/register", 
          status_code=status.HTTP_201_CREATED,
          response_model=UserRegisterOut)
async def register_user(user_data: UserRegisterIn):
    try:
        # 1. Validación y creación del usuario (operación rápida)
        new_user = await create_user_in_db(user_data)
        
        # 2. Generar IDs únicos para las tareas (garantiza idempotencia)
        email_task_id = f"email_{new_user.id}_{uuid.uuid4().hex[:8]}"
        report_task_id = f"report_{new_user.id}_{uuid.uuid4().hex[:8]}"
        
        # 3. Encolar tareas con prioridades y configuración de reintentos
        email_task = send_welcome_email.apply_async(
            args=[new_user.email, new_user.nombre],
            kwargs={'user_id': new_user.id, 'task_id': email_task_id},
            task_id=email_task_id,
            priority=8,  # Alta prioridad para emails
            retry_policy={
                'max_retries': 3,
                'interval_start': 0,
                'interval_step': 30,
                'interval_max': 300,
            }
        )
        
        report_task = generate_profile_report.apply_async(
            args=[new_user.id],
            kwargs={'task_id': report_task_id},
            task_id=report_task_id,
            priority=5,  # Prioridad media para reportes
            countdown=60,  # Delay de 1 minuto para no sobrecargar
            retry_policy={
                'max_retries': 5,
                'interval_start': 0,
                'interval_step': 60,
                'interval_max': 600,
            }
        )
        
        # 4. Registrar tareas en BD para auditoría
        await log_background_tasks(new_user.id, [
            {'task_id': email_task_id, 'type': 'send_welcome_email'},
            {'task_id': report_task_id, 'type': 'generate_profile_report'}
        ])
        
        # 5. Respuesta inmediata al cliente
        return UserRegisterOut(
            user_id=str(new_user.id),
            registered_at=new_user.created_at,
            tasks_queued=['welcome_email', 'profile_report'],
            estimated_completion="2-5 minutes"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Registration failed: {str(e)}"
        )