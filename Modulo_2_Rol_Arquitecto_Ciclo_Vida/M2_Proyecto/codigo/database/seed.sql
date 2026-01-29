-- =================================================================
-- DATOS DE SEMILLA - Sistema de Reservas
-- =================================================================
-- Este script inserta datos de prueba para desarrollo y testing
-- NO ejecutar en producción
-- =================================================================

-- Verificar que estamos en ambiente de desarrollo
DO $$
BEGIN
    IF current_database() = 'reservations_production' THEN
        RAISE EXCEPTION 'Cannot seed production database!';
    END IF;
    RAISE NOTICE 'Seeding development database...';
END $$;

-- =================================================================
-- USUARIOS DE PRUEBA
-- =================================================================
-- Password para todos: "Test123!" (hash bcrypt)
-- Generado con: bcrypt.hashpw("Test123!".encode('utf-8'), bcrypt.gensalt())

INSERT INTO users (email, password_hash, name, is_admin) VALUES
    ('admin@reservations.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5idJ8kx0JBW1u', 'Admin User', true),
    ('john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5idJ8kx0JBW1u', 'John Doe', false),
    ('jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5idJ8kx0JBW1u', 'Jane Smith', false),
    ('bob.johnson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5idJ8kx0JBW1u', 'Bob Johnson', false),
    ('alice.williams@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5idJ8kx0JBW1u', 'Alice Williams', false)
ON CONFLICT (email) DO NOTHING;

-- =================================================================
-- ESPACIOS/RECURSOS DE PRUEBA
-- =================================================================

INSERT INTO spaces (name, description, capacity, location, amenities, price_per_hour, is_active) VALUES
    (
        'Sala de Conferencias A',
        'Sala amplia con equipamiento completo para reuniones importantes',
        20,
        'Piso 3, Ala Norte',
        '["proyector", "pizarra", "video_conferencia", "wifi", "aire_acondicionado"]'::jsonb,
        50.00,
        true
    ),
    (
        'Sala de Juntas Ejecutiva',
        'Espacio premium para juntas de directorio',
        12,
        'Piso 5, Torre Principal',
        '["pantalla_4k", "sistema_audio", "video_conferencia", "wifi", "catering", "vista_panoramica"]'::jsonb,
        100.00,
        true
    ),
    (
        'Espacio Colaborativo',
        'Área abierta para trabajo en equipo',
        8,
        'Piso 2, Zona Creativa',
        '["pizarras", "wifi", "cafe", "sillas_ergonomicas"]'::jsonb,
        30.00,
        true
    ),
    (
        'Sala de Capacitación',
        'Ideal para workshops y sesiones de entrenamiento',
        30,
        'Piso 1, Edificio B',
        '["proyector", "pantallas_multiples", "wifi", "sistema_audio", "mesas_moviles"]'::jsonb,
        60.00,
        true
    ),
    (
        'Cabina de Enfoque',
        'Espacio individual para concentración',
        1,
        'Piso 2-4, Distribuidas',
        '["escritorio", "monitor", "wifi", "iluminacion_ajustable", "insonorizado"]'::jsonb,
        15.00,
        true
    ),
    (
        'Sala de Reuniones B',
        'Sala mediana para equipos de proyecto',
        10,
        'Piso 3, Ala Sur',
        '["tv", "pizarra", "wifi", "telefono_conferencia"]'::jsonb,
        40.00,
        true
    ),
    (
        'Auditorio Principal',
        'Espacio para eventos grandes y presentaciones',
        150,
        'Piso 1, Entrada Principal',
        '["escenario", "sistema_sonido_profesional", "proyectores_multiples", "luces", "streaming"]'::jsonb,
        200.00,
        true
    ),
    (
        'Sala de Innovación',
        'Equipada con tecnología de punta para brainstorming',
        15,
        'Piso 4, Zona Tech',
        '["pantallas_tactiles", "realidad_virtual", "impresora_3d", "wifi_alta_velocidad"]'::jsonb,
        80.00,
        true
    )
ON CONFLICT DO NOTHING;

-- =================================================================
-- RESERVAS DE EJEMPLO
-- =================================================================
-- Crear reservas para los próximos días (dinámico)

-- Reservas futuras
INSERT INTO reservations (user_id, space_id, start_time, end_time, status, notes) VALUES
    -- Hoy
    (2, 1, CURRENT_DATE + INTERVAL '10 hours', CURRENT_DATE + INTERVAL '12 hours', 'active', 'Reunión mensual de ventas'),
    (3, 3, CURRENT_DATE + INTERVAL '14 hours', CURRENT_DATE + INTERVAL '16 hours', 'active', 'Sesión de brainstorming'),
    (4, 5, CURRENT_DATE + INTERVAL '9 hours', CURRENT_DATE + INTERVAL '11 hours', 'active', 'Trabajo concentrado'),
    
    -- Mañana
    (2, 2, CURRENT_DATE + INTERVAL '1 day 10 hours', CURRENT_DATE + INTERVAL '1 day 13 hours', 'active', 'Presentación de Q4'),
    (3, 4, CURRENT_DATE + INTERVAL '1 day 15 hours', CURRENT_DATE + INTERVAL '1 day 17 hours', 'active', 'Training de nuevo software'),
    (5, 6, CURRENT_DATE + INTERVAL '1 day 11 hours', CURRENT_DATE + INTERVAL '1 day 12 hours', 'active', 'Daily standup extendido'),
    
    -- Pasado mañana
    (4, 7, CURRENT_DATE + INTERVAL '2 days 9 hours', CURRENT_DATE + INTERVAL '2 days 12 hours', 'active', 'All-hands meeting'),
    (5, 8, CURRENT_DATE + INTERVAL '2 days 14 hours', CURRENT_DATE + INTERVAL '2 days 17 hours', 'active', 'Hackathon interno'),
    
    -- Próxima semana
    (2, 1, CURRENT_DATE + INTERVAL '7 days 10 hours', CURRENT_DATE + INTERVAL '7 days 11 hours', 'active', 'Kick-off meeting'),
    (3, 3, CURRENT_DATE + INTERVAL '8 days 15 hours', CURRENT_DATE + INTERVAL '8 days 17 hours', 'active', 'Sprint planning'),
    (4, 2, CURRENT_DATE + INTERVAL '9 days 13 hours', CURRENT_DATE + INTERVAL '9 days 16 hours', 'active', 'Client presentation'),
    (5, 4, CURRENT_DATE + INTERVAL '10 days 10 hours', CURRENT_DATE + INTERVAL '10 days 13 hours', 'active', 'Workshop de liderazgo')
ON CONFLICT DO NOTHING;

-- Reservas pasadas (completadas)
INSERT INTO reservations (user_id, space_id, start_time, end_time, status, notes) VALUES
    (2, 1, CURRENT_DATE - INTERVAL '2 days 10 hours', CURRENT_DATE - INTERVAL '2 days 12 hours', 'completed', 'Reunión retrospectiva'),
    (3, 3, CURRENT_DATE - INTERVAL '3 days 14 hours', CURRENT_DATE - INTERVAL '3 days 16 hours', 'completed', 'Design review'),
    (4, 6, CURRENT_DATE - INTERVAL '5 days 11 hours', CURRENT_DATE - INTERVAL '5 days 13 hours', 'completed', 'Entrevistas técnicas'),
    (5, 4, CURRENT_DATE - INTERVAL '7 days 9 hours', CURRENT_DATE - INTERVAL '7 days 12 hours', 'completed', 'Onboarding session')
ON CONFLICT DO NOTHING;

-- Algunas reservas canceladas
INSERT INTO reservations (user_id, space_id, start_time, end_time, status, notes) VALUES
    (2, 2, CURRENT_DATE - INTERVAL '1 day 15 hours', CURRENT_DATE - INTERVAL '1 day 17 hours', 'cancelled', 'Reunión pospuesta'),
    (3, 5, CURRENT_DATE + INTERVAL '5 days 10 hours', CURRENT_DATE + INTERVAL '5 days 11 hours', 'cancelled', 'Cambio de planes')
ON CONFLICT DO NOTHING;

-- =================================================================
-- ESTADÍSTICAS Y VERIFICACIÓN
-- =================================================================

-- Mostrar resumen de datos insertados
DO $$
DECLARE
    user_count INTEGER;
    space_count INTEGER;
    reservation_count INTEGER;
    active_reservation_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM users;
    SELECT COUNT(*) INTO space_count FROM spaces WHERE is_active = TRUE;
    SELECT COUNT(*) INTO reservation_count FROM reservations;
    SELECT COUNT(*) INTO active_reservation_count FROM reservations WHERE status = 'active';
    
    RAISE NOTICE '================================';
    RAISE NOTICE 'DATABASE SEEDING COMPLETED';
    RAISE NOTICE '================================';
    RAISE NOTICE 'Users created: %', user_count;
    RAISE NOTICE 'Active spaces: %', space_count;
    RAISE NOTICE 'Total reservations: %', reservation_count;
    RAISE NOTICE 'Active reservations: %', active_reservation_count;
    RAISE NOTICE '================================';
    RAISE NOTICE 'Test credentials:';
    RAISE NOTICE '  Email: admin@reservations.com';
    RAISE NOTICE '  Password: Test123!';
    RAISE NOTICE '================================';
END $$;

-- Crear una función útil para desarrollo
CREATE OR REPLACE FUNCTION reset_demo_data()
RETURNS VOID AS $$
BEGIN
    TRUNCATE reservations, spaces, users RESTART IDENTITY CASCADE;
    RAISE NOTICE 'All data deleted. Re-run seed script to restore.';
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION reset_demo_data() IS 'DEVELOPMENT ONLY: Deletes all data from tables';