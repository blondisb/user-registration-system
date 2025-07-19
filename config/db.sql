-- Tabla principal de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre TEXT NOT NULL,
    telefono TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Tabla de auditoría de tareas (para monitoreo y debugging)
CREATE TABLE background_tasks_audit (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    task_id TEXT UNIQUE NOT NULL,
    task_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued', 
    -- queued | in_progress | completed | failed | retrying
    payload JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3
);

-- Tabla de resultados de tareas (para consultas posteriores)
CREATE TABLE task_results (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    task_id TEXT NOT NULL,
    task_type TEXT NOT NULL,
    result_data JSONB,
    file_path TEXT, -- Para archivos generados como PDFs
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Índices para optimización
CREATE INDEX idx_background_tasks_status ON background_tasks_audit(status);
CREATE INDEX idx_background_tasks_user_id ON background_tasks_audit(user_id);
CREATE INDEX idx_background_tasks_task_type ON background_tasks_audit(task_type);