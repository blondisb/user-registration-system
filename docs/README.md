# 1. Instalar dependencias
pip install -r requirements/dev.txt

# 2. Configurar variables de entorno
cp .env.example .env.local

# 3. Inicializar base de datos
python scripts/init_db.py

# 4. Ejecutar migraciones
alembic upgrade head

# 5. Levantar servicios (3 terminales):
make run-api      # Terminal 1: FastAPI en :8000
make run-worker   # Terminal 2: Celery worker
make run-flower   # Terminal 3: Flower monitoring en :5555
















docker-compose up --build
# Todo levantado automáticamente:
# - API: localhost:8000
# - Worker: background
# - Redis: localhost:6379  
# - PostgreSQL: localhost:5432
# - Flower: localhost:5555






# 🔧 Comandos principales (Makefile):
make install          # Instalar dependencias
make run-api         # Ejecutar FastAPI
make run-worker      # Ejecutar Celery worker
make run-monitoring  # Ejecutar Flower + Prometheus
make test           # Ejecutar tests
make migrate        # Ejecutar migraciones
make docker-up      # Levantar todo con Docker
make lint          # Linting y formateo