# Código Fuente - Sistema de Reservas

## 📁 Estructura del Proyecto

```
codigo/
├── README.md                      # Este archivo
├── docker-compose.yml             # Orquestación de todos los servicios
├── .env.example                   # Template de variables de entorno
├── .env                          # Variables de entorno (crear desde .env.example)
│
├── gateway/                       # API Gateway (NGINX)
│   └── nginx.conf                # Configuración de routing
│
├── database/                      # Scripts de base de datos
│   ├── init.sql                  # Schema inicial
│   └── seed.sql                  # Datos de prueba
│
├── auth-service/                  # Servicio de Autenticación
│   ├── main.py                   # Código principal
│   ├── Dockerfile                # Imagen Docker
│   ├── requirements.txt          # Dependencias Python
│   └── tests/                    # Tests unitarios
│
├── users-service/                 # Servicio de Usuarios
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│
├── reservations-service/          # Servicio de Reservas
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│
└── spaces-service/                # Servicio de Espacios
    ├── main.py
    ├── Dockerfile
    ├── requirements.txt
    └── tests/
```

---

## 🚀 Inicio Rápido

### 1. Prerequisitos

Asegúrate de tener instalado:
- Docker >= 20.10
- Docker Compose >= 2.0
- Git

Verificar instalación:
```bash
docker --version
docker-compose --version
```

### 2. Configuración Inicial

```bash
# 1. Clonar el repositorio (si aún no lo has hecho)
git clone https://github.com/D-Araya/fundamentos_arquitectura_cloud.git
cd fundamentos_arquitectura_cloud/Modulo_2_Arquitectura_Software/M2_AE4_Pilares_Fundamentales/codigo

# 2. Crear archivo .env desde el template
cp .env.example .env

# 3. Editar .env y cambiar los valores sensibles
nano .env  # o tu editor preferido

# IMPORTANTE: Cambiar al menos:
# - POSTGRES_PASSWORD
# - JWT_SECRET (generar con: python3 -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 3. Levantar Todos los Servicios

```bash
# Build de las imágenes
docker-compose build

# Iniciar todos los contenedores
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 4. Verificar que Todo Funciona

```bash
# Health check del gateway
curl http://localhost/health

# Health check de cada servicio
curl http://localhost/api/auth/health
curl http://localhost/api/users/health
curl http://localhost/api/reservations/health
curl http://localhost/api/spaces/health
```

Si todos responden con `"status": "healthy"`, ¡todo está funcionando! ✅

---

## 📖 Documentación de APIs

Una vez que los servicios estén corriendo, puedes acceder a la documentación interactiva:

- **Swagger UI**: http://localhost/api/auth/docs
- **ReDoc**: http://localhost/api/auth/redoc

---

## 🧪 Probar el Sistema

### Ejemplo 1: Registrar un Usuario

```bash
curl -X POST http://localhost/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Usuario de Prueba"
  }'
```

**Respuesta esperada**:
```json
{
  "user": {
    "id": 1,
    "email": "test@example.com",
    "name": "Usuario de Prueba",
    "is_admin": false
  },
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Ejemplo 2: Login

```bash
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### Ejemplo 3: Crear una Reserva

```bash
# Primero, guardar el token del login anterior
TOKEN="tu_token_aqui"

# Crear reserva
curl -X POST http://localhost/api/reservations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "start_time": "2026-01-20T10:00:00",
    "end_time": "2026-01-20T12:00:00"
  }'
```

### Ejemplo 4: Listar Espacios Disponibles

```bash
curl http://localhost/api/spaces
```

---

## 🔧 Comandos Útiles

### Gestión de Contenedores

```bash
# Ver estado de todos los servicios
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs -f auth-service

# Reiniciar un servicio
docker-compose restart auth-service

# Detener todos los servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar TODO (incluyendo volúmenes)
docker-compose down -v
```

### Database

```bash
# Conectarse a PostgreSQL
docker-compose exec postgres psql -U reservations_user -d reservations

# Ver tablas
docker-compose exec postgres psql -U reservations_user -d reservations -c "\dt"

# Ver usuarios de prueba
docker-compose exec postgres psql -U reservations_user -d reservations -c "SELECT id, email, name FROM users;"

# Backup de la base de datos
docker-compose exec postgres pg_dump -U reservations_user reservations > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U reservations_user reservations < backup.sql
```

### Redis

```bash
# Conectarse a Redis
docker-compose exec redis redis-cli

# Ver todas las keys
docker-compose exec redis redis-cli KEYS "*"

# Limpiar caché
docker-compose exec redis redis-cli FLUSHALL
```

### Debugging

```bash
# Ejecutar bash en un contenedor
docker-compose exec auth-service bash

# Ver uso de recursos
docker stats

# Inspeccionar un contenedor
docker inspect codigo-auth-service-1
```

---

## 🧪 Ejecutar Tests

### Tests Unitarios

```bash
# Todos los servicios
docker-compose exec auth-service pytest -v
docker-compose exec users-service pytest -v
docker-compose exec reservations-service pytest -v
docker-compose exec spaces-service pytest -v

# Con cobertura
docker-compose exec auth-service pytest --cov --cov-report=html
```

### Tests de Carga (requiere k6 instalado localmente)

```bash
# Instalar k6
# macOS: brew install k6
# Linux: sudo snap install k6

# Ejecutar test de carga
k6 run tests/load/sustained-load.js
```

---

## 🛠️ Desarrollo Local (Sin Docker)

Si prefieres desarrollar sin Docker:

### 1. Instalar Dependencias del Sistema

```bash
# PostgreSQL y Redis
# macOS:
brew install postgresql redis

# Ubuntu/Debian:
sudo apt-get install postgresql redis-server
```

### 2. Crear Base de Datos

```bash
# Crear usuario y database
psql postgres -c "CREATE USER reservations_user WITH PASSWORD 'yourpassword';"
psql postgres -c "CREATE DATABASE reservations OWNER reservations_user;"

# Ejecutar migrations
psql -U reservations_user -d reservations -f database/init.sql
psql -U reservations_user -d reservations -f database/seed.sql
```

### 3. Ejecutar un Servicio

```bash
cd auth-service

# Crear virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://reservations_user:yourpassword@localhost:5432/reservations"
export JWT_SECRET="your-secret-key"
export REDIS_URL="redis://localhost:6379"

# Ejecutar servicio
uvicorn main:app --reload --port 8001
```

Repetir para cada servicio en puertos diferentes (8001, 8002, 8003, 8004).

---

## 🐛 Troubleshooting

### Problema: Puerto 80 ocupado

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8080:80"  # Usar 8080 en lugar de 80

# Luego acceder a http://localhost:8080
```

### Problema: Containers se reinician

```bash
# Ver logs del servicio problemático
docker-compose logs auth-service

# Verificar salud de base de datos
docker-compose ps postgres
```

### Problema: Cambios en código no se reflejan

```bash
# Rebuild del servicio
docker-compose build auth-service
docker-compose up -d --force-recreate auth-service
```

### Problema: Base de datos no se inicializa

```bash
# Eliminar volúmenes y recrear
docker-compose down -v
docker-compose up -d
```

---

## 📊 Arquitectura de los Servicios

### Auth Service (Puerto 8001)

**Responsabilidad**: Autenticación y gestión de tokens

**Endpoints**:
- `POST /register` - Registrar usuario
- `POST /login` - Autenticar
- `POST /refresh` - Renovar token
- `POST /validate` - Validar token (interno)
- `GET /health` - Health check

### Users Service (Puerto 8002)

**Responsabilidad**: Gestión de perfiles de usuario

**Endpoints**:
- `GET /me` - Perfil actual
- `PUT /me` - Actualizar perfil
- `DELETE /me` - Eliminar cuenta
- `GET /health` - Health check

### Reservations Service (Puerto 8003)

**Responsabilidad**: CRUD de reservas

**Endpoints**:
- `POST /` - Crear reserva
- `GET /` - Listar mis reservas
- `GET /{id}` - Detalle de reserva
- `DELETE /{id}` - Cancelar reserva
- `GET /health` - Health check

### Spaces Service (Puerto 8004)

**Responsabilidad**: Gestión de espacios reservables

**Endpoints**:
- `GET /` - Listar espacios
- `GET /{id}` - Detalle de espacio
- `GET /{id}/availability` - Verificar disponibilidad
- `POST /` - Crear espacio (admin)
- `GET /health` - Health check

---

## 🔒 Seguridad

### Variables de Entorno Sensibles

**NUNCA** commitear el archivo `.env` al repositorio.

Valores que DEBES cambiar en producción:
- `POSTGRES_PASSWORD`
- `JWT_SECRET`

### Generar JWT Secret Seguro

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Credenciales de Prueba

Los datos de semilla incluyen usuarios de prueba:

- **Email**: `admin@reservations.com`
- **Password**: `Test123!`
- **Rol**: Administrador

**⚠️ ELIMINAR en producción**

---

## 📝 Notas Adicionales

### Puertos Utilizados

- **80**: API Gateway (NGINX)
- **5432**: PostgreSQL (solo interno)
- **6379**: Redis (solo interno)
- **8000**: Servicios internos (no expuestos)

### Volúmenes Persistentes

Los datos se almacenan en volúmenes Docker:
- `postgres-data`: Base de datos PostgreSQL
- `redis-data`: Caché de Redis

Para backup, respaldar estos volúmenes.

### Escalamiento

Escalar un servicio:
```bash
docker-compose up -d --scale reservations-service=3
```

NGINX automáticamente balanceará la carga.

---

## 🚀 Próximos Pasos

1. ✅ Explorar la documentación Swagger en `/docs`
2. ✅ Probar todos los endpoints con Postman o curl
3. ✅ Revisar los logs para entender el flujo
4. ✅ Ejecutar los tests unitarios
5. ✅ Modificar configuraciones y experimentar

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/D-Araya/fundamentos_arquitectura_cloud/issues)
- **Documentación**: Ver `../documentos/` para guías detalladas

---

**Última actualización**: Enero 2026  
**Autor**: Daniel Araya