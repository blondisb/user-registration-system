from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from datetime import datetime

class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    telefono: str = None
    metadata: Dict[str, Any] = {}

class UserRegisterOut(BaseModel):
    user_id: str
    registered_at: datetime
    tasks_queued: list[str]
    estimated_completion: str