-- =================================================================
-- SCHEMA DE BASE DE DATOS - Sistema de Reservas
-- =================================================================
-- Este script inicializa la estructura completa de la base de datos
-- Incluye: tablas, índices, constraints, triggers y funciones
-- =================================================================

-- Configuración inicial
SET client_encoding = 'UTF8';
SET timezone = 'UTC';

-- =================================================================
-- TABLA: users
-- Almacena información de usuarios del sistema
-- =================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints adicionales
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    CONSTRAINT name_not_empty CHECK (LENGTH(TRIM(name)) > 0)
);

-- Índices para users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC);

-- Comentarios
COMMENT ON TABLE users IS 'Usuarios registrados en el sistema';
COMMENT ON COLUMN users.email IS 'Email único del usuario (usado para login)';
COMMENT ON COLUMN users.password_hash IS 'Hash bcrypt de la contraseña';
COMMENT ON COLUMN users.is_active IS 'Usuario activo o desactivado';
COMMENT ON COLUMN users.is_admin IS 'Permisos de administrador';

-- =================================================================
-- TABLA: spaces
-- Almacena espacios/recursos disponibles para reserva
-- =================================================================
CREATE TABLE IF NOT EXISTS spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    capacity INTEGER NOT NULL,
    location VARCHAR(255),
    amenities JSONB DEFAULT '[]'::jsonb,
    price_per_hour DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT capacity_positive CHECK (capacity > 0),
    CONSTRAINT price_non_negative CHECK (price_per_hour >= 0),
    CONSTRAINT name_not_empty CHECK (LENGTH(TRIM(name)) > 0)
);

-- Índices para spaces
CREATE INDEX IF NOT EXISTS idx_spaces_active ON spaces(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_spaces_capacity ON spaces(capacity);
CREATE INDEX IF NOT EXISTS idx_spaces_amenities ON spaces USING GIN (amenities);
CREATE INDEX IF NOT EXISTS idx_spaces_name ON spaces(name);

-- Comentarios
COMMENT ON TABLE spaces IS 'Espacios y recursos disponibles para reserva';
COMMENT ON COLUMN spaces.amenities IS 'Array JSON de amenidades (ej: ["wifi", "proyector", "pizarra"])';
COMMENT ON COLUMN spaces.price_per_hour IS 'Precio por hora de uso del espacio';

-- =================================================================
-- TABLA: reservations
-- Almacena las reservas realizadas por usuarios
-- =================================================================
CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    space_id INTEGER NOT NULL REFERENCES spaces(id) ON DELETE CASCADE,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) DEFAULT 'active' NOT NULL,
    total_price DECIMAL(10, 2),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_time_range CHECK (end_time > start_time),
    CONSTRAINT valid_status CHECK (status IN ('active', 'cancelled', 'completed')),
    CONSTRAINT minimum_duration CHECK (EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800), -- mínimo 30 minutos
    CONSTRAINT total_price_non_negative CHECK (total_price IS NULL OR total_price >= 0)
);

-- Índices para reservations
CREATE INDEX IF NOT EXISTS idx_reservations_user ON reservations(user_id);
CREATE INDEX IF NOT EXISTS idx_reservations_space ON reservations(space_id);
CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);
CREATE INDEX IF NOT EXISTS idx_reservations_time_range ON reservations(start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_reservations_start_time ON reservations(start_time DESC);
CREATE INDEX IF NOT EXISTS idx_reservations_space_time ON reservations(space_id, start_time, end_time) 
    WHERE status = 'active';

-- Índice compuesto para búsquedas de disponibilidad (query optimization)
CREATE INDEX IF NOT EXISTS idx_reservations_availability ON reservations(space_id, status, start_time, end_time)
    WHERE status = 'active';

-- Comentarios
COMMENT ON TABLE reservations IS 'Reservas de espacios realizadas por usuarios';
COMMENT ON COLUMN reservations.status IS 'Estado: active (activa), cancelled (cancelada), completed (completada)';
COMMENT ON COLUMN reservations.total_price IS 'Precio total calculado de la reserva';
COMMENT ON COLUMN reservations.notes IS 'Notas adicionales de la reserva';

-- =================================================================
-- FUNCIONES Y TRIGGERS
-- =================================================================

-- Función para actualizar automáticamente updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spaces_updated_at 
    BEFORE UPDATE ON spaces
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reservations_updated_at 
    BEFORE UPDATE ON reservations
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Función para calcular precio total de reserva
CREATE OR REPLACE FUNCTION calculate_reservation_price()
RETURNS TRIGGER AS $$
DECLARE
    hours_duration DECIMAL;
    hourly_rate DECIMAL;
BEGIN
    -- Calcular duración en horas (redondeado hacia arriba)
    hours_duration := CEIL(EXTRACT(EPOCH FROM (NEW.end_time - NEW.start_time)) / 3600.0);
    
    -- Obtener precio por hora del espacio
    SELECT price_per_hour INTO hourly_rate 
    FROM spaces 
    WHERE id = NEW.space_id;
    
    -- Calcular precio total
    NEW.total_price := hours_duration * hourly_rate;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para calcular precio automáticamente
CREATE TRIGGER calculate_price_before_insert 
    BEFORE INSERT ON reservations
    FOR EACH ROW 
    EXECUTE FUNCTION calculate_reservation_price();

-- Función para validar solapamiento de reservas
CREATE OR REPLACE FUNCTION check_reservation_overlap()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si existe una reserva activa que se solape
    IF EXISTS (
        SELECT 1 
        FROM reservations 
        WHERE space_id = NEW.space_id
          AND status = 'active'
          AND id != COALESCE(NEW.id, 0)  -- Excluir la misma reserva en UPDATEs
          AND (
              (NEW.start_time >= start_time AND NEW.start_time < end_time) OR
              (NEW.end_time > start_time AND NEW.end_time <= end_time) OR
              (NEW.start_time <= start_time AND NEW.end_time >= end_time)
          )
    ) THEN
        RAISE EXCEPTION 'Reservation conflict: Space is already booked for this time range'
            USING ERRCODE = '23P01';  -- Código de error de constraint violation
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para validar solapamiento
CREATE TRIGGER prevent_reservation_overlap 
    BEFORE INSERT OR UPDATE ON reservations
    FOR EACH ROW 
    EXECUTE FUNCTION check_reservation_overlap();

-- =================================================================
-- VISTAS ÚTILES
-- =================================================================

-- Vista de reservas con información completa
CREATE OR REPLACE VIEW reservations_full AS
SELECT 
    r.id,
    r.user_id,
    u.name AS user_name,
    u.email AS user_email,
    r.space_id,
    s.name AS space_name,
    s.location AS space_location,
    r.start_time,
    r.end_time,
    EXTRACT(EPOCH FROM (r.end_time - r.start_time)) / 3600.0 AS duration_hours,
    r.status,
    r.total_price,
    r.notes,
    r.created_at,
    r.updated_at
FROM reservations r
JOIN users u ON r.user_id = u.id
JOIN spaces s ON r.space_id = s.id;

COMMENT ON VIEW reservations_full IS 'Vista completa de reservas con información de usuario y espacio';

-- Vista de espacios disponibles
CREATE OR REPLACE VIEW available_spaces AS
SELECT 
    s.*,
    COUNT(r.id) AS total_reservations,
    COALESCE(SUM(CASE WHEN r.status = 'active' THEN 1 ELSE 0 END), 0) AS active_reservations
FROM spaces s
LEFT JOIN reservations r ON s.id = r.space_id
WHERE s.is_active = TRUE
GROUP BY s.id;

COMMENT ON VIEW available_spaces IS 'Espacios activos con estadísticas de reservas';

-- =================================================================
-- ESTADÍSTICAS Y METADATA
-- =================================================================

-- Función para obtener estadísticas del sistema
CREATE OR REPLACE FUNCTION get_system_stats()
RETURNS JSON AS $$
DECLARE
    stats JSON;
BEGIN
    SELECT json_build_object(
        'total_users', (SELECT COUNT(*) FROM users WHERE is_active = TRUE),
        'total_spaces', (SELECT COUNT(*) FROM spaces WHERE is_active = TRUE),
        'active_reservations', (SELECT COUNT(*) FROM reservations WHERE status = 'active'),
        'total_reservations', (SELECT COUNT(*) FROM reservations),
        'database_size', pg_database_size(current_database())
    ) INTO stats;
    
    RETURN stats;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_system_stats() IS 'Retorna estadísticas generales del sistema';

-- =================================================================
-- GRANTS (Permisos - ajustar según necesidad)
-- =================================================================

-- En producción, crear roles específicos con permisos limitados
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_role;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_role;

-- =================================================================
-- INFORMACIÓN FINAL
-- =================================================================

-- Insertar metadata de la versión del schema
CREATE TABLE IF NOT EXISTS schema_version (
    version VARCHAR(20) PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO schema_version (version, description) 
VALUES ('1.0.0', 'Initial schema - Users, Spaces, Reservations')
ON CONFLICT (version) DO NOTHING;

-- Log de finalización
DO $$
BEGIN
    RAISE NOTICE 'Database schema initialized successfully';
    RAISE NOTICE 'Version: 1.0.0';
    RAISE NOTICE 'Tables created: users, spaces, reservations';
    RAISE NOTICE 'Triggers enabled for: updated_at, price calculation, overlap validation';
END $$;