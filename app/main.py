from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.middleware import setup_middleware

app = FastAPI(title="User Registration System")
setup_middleware(app)
app.include_router(api_router, prefix="/api/v1")