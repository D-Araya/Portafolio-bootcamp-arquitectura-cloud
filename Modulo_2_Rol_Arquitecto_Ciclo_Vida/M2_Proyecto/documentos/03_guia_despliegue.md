# Guía de Despliegue - Sistema de Reservas

## 📋 Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación Paso a Paso](#instalación-paso-a-paso)
3. [Configuración](#configuración)
4. [Despliegue Local](#despliegue-local)
5. [Verificación](#verificación)
6. [Comandos Útiles](#comandos-útiles)
7. [Troubleshooting](#troubleshooting)
8. [Despliegue en Producción](#despliegue-en-producción)

---

## Requisitos Previos

### Software Requerido

| Software | Versión Mínima | Verificación | Instalación |
|----------|----------------|--------------|-------------|
| **Docker Desktop** | 20.10+ | `docker --version` | [docker.com](https://docs.docker.com/get-docker/) |
| **Docker Compose** | 2.0+ | `docker-compose --version` | Incluido con Docker Desktop |
| **Git** | 2.30+ | `git --version` | [git-scm.com](https://git-scm.com/) |
| **WSL 2** (Windows) | - | `wsl --status` | [Recomendado](https://docs.microsoft.com/en-us/windows/wsl/install) |

### Software Opcional (Para Desarrollo)

| Software | Propósito |
|----------|-----------|
| **Python 3.11+** | Desarrollo local sin Docker |
| **PostgreSQL Client** | Inspección directa de BD |
| **Redis CLI** | Debug de caché |
| **k6** | Pruebas de carga |
| **Postman** | Testing de APIs |

### Recursos del Sistema

**Mínimos**:
- CPU: 2 cores
- RAM: 4 GB
- Disco: 5 GB disponibles

**Recomendados**:
- CPU: 4 cores
- RAM: 8 GB
- Disco: 10 GB disponibles

---

## Instalación Paso a Paso

### 1. Clonar el Repositorio

#### Windows (PowerShell)

```powershell
# Opción 1: HTTPS
git clone https://github.com/D-Araya/fundamentos_arquitectura_cloud.git

# Opción 2: SSH (si tienes SSH keys configuradas)
git clone git@github.com:D-Araya/fundamentos_arquitectura_cloud.git

# Navegar al directorio del proyecto
cd fundamentos_arquitectura_cloud\Modulo_2_Rol_Arquitecto_Ciclo_Vida\M2_Proyecto
```

#### Linux/macOS

```bash
# Opción 1: HTTPS
git clone https://github.com/D-Araya/fundamentos_arquitectura_cloud.git

# Navegar al directorio del proyecto
cd fundamentos_arquitectura_cloud/Modulo_2_Rol_Arquitecto_Ciclo_Vida/M2_Proyecto
```

### 2. Verificar Estructura del Proyecto

#### Windows

```powershell
tree /F
```

#### Linux/macOS

```bash
tree -L 3
```

Deberías ver:
```
M2_Proyecto/
├── README.md
├── documentos/
├── imagenes/
├── codigo/
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── gateway/
│   ├── database/
│   ├── auth-service/
│   ├── users-service/
│   ├── reservations-service/
│   └── spaces-service/
└── tests/
```

### 3. Navegar al Directorio de Código

#### Windows

```powershell
cd codigo
```

#### Linux/macOS

```bash
cd codigo
```

---

## Configuración

### 1. Variables de Entorno

#### Windows

```powershell
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar con tu editor favorito
notepad .env  # o code .env para VS Code
```

#### Linux/macOS

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tu editor favorito
nano .env  # o vim .env, code .env
```

**Contenido de `.env`**:

```bash
# Database Configuration
POSTGRES_USER=reservations_user
POSTGRES_PASSWORD=SecurePassword123!  # CAMBIAR EN PRODUCCIÓN
POSTGRES_DB=reservations
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Database URL para los servicios
DATABASE_URL=postgresql://reservations_user:SecurePassword123!@postgres:5432/reservations

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_URL=redis://redis:6379

# JWT Configuration
JWT_SECRET=tu-secret-key-super-segura-cambiala-en-produccion  # CAMBIAR
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Application Configuration
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
```

### 2. Generar Secret Key Seguro (Producción)

#### Windows

```powershell
# Generar secret key aleatorio
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Linux/macOS

```bash
# Generar secret key aleatorio
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Copiar el output y reemplazar `JWT_SECRET` en `.env`**

---

## Despliegue Local

### Método 1: Docker Compose (Recomendado)

#### Paso 1: Build de las Imágenes

**Windows**:
```powershell
docker-compose build
```

**Linux/macOS**:
```bash
docker-compose build
```

**Salida esperada**:
```
[+] Building 45.2s (48/48) FINISHED
 => [auth-service internal] load build definition
 => [users-service internal] load build definition
 ...
```

#### Paso 2: Levantar los Servicios

**Windows**:
```powershell
# Iniciar en background
docker-compose up -d

# O ver logs en tiempo real
docker-compose up
```

**Linux/macOS**:
```bash
# Iniciar en background
docker-compose up -d

# O ver logs en tiempo real
docker-compose up
```

**Salida esperada**:
```
[+] Running 7/7
 ✔ Network codigo_app-network           Created
 ✔ Container codigo-postgres-1          Started
 ✔ Container codigo-redis-1             Started
 ✔ Container codigo-auth-service-1      Started
 ✔ Container codigo-users-service-1     Started
 ✔ Container codigo-reservations-service-1  Started
 ✔ Container codigo-spaces-service-1    Started
 ✔ Container codigo-gateway-1           Started
```

#### Paso 3: Verificar Estado

```powershell
# Windows y Linux
docker-compose ps
```

**Salida esperada** (todos con status `Up (healthy)`):
```
NAME                              STATUS              PORTS
reservations-auth                 Up (healthy)        8000/tcp
reservations-gateway              Up (healthy)        0.0.0.0:80->80/tcp
reservations-postgres             Up (healthy)        5432/tcp
reservations-redis                Up (healthy)        6379/tcp
reservations-reservations         Up (healthy)        8000/tcp
reservations-spaces               Up (healthy)        8000/tcp
reservations-users                Up (healthy)        8000/tcp
```

⚠️ **Nota**: Los health checks pueden tardar 30-40 segundos en pasar inicialmente.

---

## Verificación

### 1. Health Checks

#### Windows

```powershell
# Health check del gateway
curl http://localhost/health

# Health check de cada servicio
curl http://localhost/api/auth/health
curl http://localhost/api/users/health
curl http://localhost/api/reservations/health
curl http://localhost/api/spaces/health
```

#### Linux/macOS

```bash
# Health check del gateway
curl http://localhost/health

# Health check de cada servicio
curl http://localhost/api/auth/health
curl http://localhost/api/users/health
curl http://localhost/api/reservations/health
curl http://localhost/api/spaces/health
```

**Respuesta esperada** (cada uno):
```json
{
  "status": "healthy",
  "service": "auth-service",
  "timestamp": "2026-01-19T10:30:00.000000",
  "database": "connected",
  "cache": "connected"
}
```

### 2. Documentación Interactiva

Abrir en el navegador:

- **Swagger UI**: http://localhost/api/auth/docs
- **ReDoc**: http://localhost/api/auth/redoc
- **OpenAPI Spec**: http://localhost/openapi.json

### 3. Test de Flujo Completo

#### A. Registrar un Usuario

**Windows (PowerShell)**:
```powershell
curl -X POST http://localhost/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"SecurePass123!\",\"name\":\"Usuario de Prueba\"}'
```

**Linux/macOS**:
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
  "token_type": "bearer"
}
```

#### B. Login

**Windows**:
```powershell
curl -X POST http://localhost/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"SecurePass123!\"}'
```

**Linux/macOS**:
```bash
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'
```

#### C. Crear una Reserva

**Windows**:
```powershell
$token = "tu_token_aqui"

curl -X POST http://localhost/api/reservations `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d '{\"space_id\":1,\"start_time\":\"2026-01-20T10:00:00\",\"end_time\":\"2026-01-20T12:00:00\"}'
```

**Linux/macOS**:
```bash
TOKEN="tu_token_aqui"

curl -X POST http://localhost/api/reservations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "start_time": "2026-01-20T10:00:00",
    "end_time": "2026-01-20T12:00:00"
  }'
```

### 4. Verificar Logs

```powershell
# Windows y Linux - Todos iguales

# Ver logs de todos los servicios
docker-compose logs

# Seguir logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f auth-service

# Últimas 100 líneas
docker-compose logs --tail=100
```

---

## Comandos Útiles

### Gestión de Contenedores

```powershell
# Windows y Linux - Mismos comandos

# Ver estado de todos los servicios
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs -f auth-service

# Reiniciar un servicio
docker-compose restart auth-service

# Detener todos los servicios
docker-compose stop

# Detener y eliminar containers
docker-compose down

# Detener y eliminar TODO (incluyendo volúmenes) ⚠️
docker-compose down -v

# Rebuild de un servicio específico
docker-compose build auth-service --no-cache

# Escalar un servicio
docker-compose up -d --scale reservations-service=3
```

### Database

```powershell
# Windows y Linux - Mismos comandos

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
# Conectarse a Redis CLI
docker-compose exec redis redis-cli

# Ver todas las keys
docker-compose exec redis redis-cli KEYS "*"

# Limpiar cache
docker-compose exec redis redis-cli FLUSHALL
```

### Debugging

```powershell
# Ejecutar bash en un contenedor (Linux containers)
docker-compose exec auth-service sh  # Alpine usa sh, no bash

# Ver uso de recursos
docker stats

# Inspeccionar un contenedor
docker inspect reservations-auth
```

---

## Troubleshooting

### Problema 1: Puerto 80 Ya Está en Uso

**Síntoma**:
```
Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
```

**Solución**:

**Windows**:
```powershell
# Identificar qué usa el puerto 80
netstat -ano | findstr :80

# Opción: Cambiar puerto del gateway
# Editar docker-compose.yml:
# ports:
#   - "8080:80"  # Usar 8080 en lugar de 80

# Acceder entonces a http://localhost:8080
```

**Linux/macOS**:
```bash
# Identificar qué usa el puerto 80
sudo lsof -i :80

# Cambiar puerto en docker-compose.yml
```

### Problema 2: Containers Se Reinician Constantemente

**Síntoma**:
```
docker-compose ps muestra "Restarting"
```

**Diagnóstico**:
```powershell
# Ver logs del servicio problemático
docker-compose logs auth-service

# Revisar últimas líneas antes del crash
docker-compose logs --tail=50 auth-service
```

**Causas comunes**:
- Error en variables de entorno (revisar `.env`)
- Base de datos no disponible (esperar a que postgres esté healthy)
- Error en el código (revisar logs)

### Problema 3: Health Checks Failing

**Síntoma**:
```
Services showing "unhealthy"
```

**Solución**:
```powershell
# Los health checks toman 30-40 segundos
# Esperar y verificar nuevamente
timeout /t 40  # Windows
sleep 40       # Linux/macOS

docker-compose ps

# Si aún fallan, ver logs
docker-compose logs postgres
docker-compose logs redis
```

### Problema 4: Cambios en Código No Se Reflejan

**Solución**:
```powershell
# Rebuild del servicio específico
docker-compose build auth-service --no-cache

# Recrear el container
docker-compose up -d --force-recreate auth-service
```

### Problema 5: Tests Fallan

**Solución**:
```powershell
# Verificar que requirements.txt está actualizado
docker-compose exec auth-service pip list

# Rebuild si es necesario
docker-compose build auth-service --no-cache
docker-compose up -d
```

### Problema 6: Out of Memory (Windows)

**Síntoma**:
Sistema lento, containers se cierran inesperadamente

**Solución**:
```
1. Abrir Docker Desktop
2. Settings > Resources
3. Aumentar memoria a mínimo 6GB (recomendado 8GB)
4. Aplicar y reiniciar
```

---

## Despliegue en Producción

### Preparación

#### 1. Variables de Entorno de Producción

```bash
# Crear .env.production
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING

# Generar secrets seguros
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(16))")

# NO usar localhost
ALLOWED_ORIGINS=https://tusitio.com,https://www.tusitio.com
```

#### 2. Configuración de Seguridad

- ✅ HTTPS obligatorio (usar Nginx con Let's Encrypt)
- ✅ Secrets en gestores (AWS Secrets Manager, HashiCorp Vault)
- ✅ Network policies restrictivas
- ✅ Resource limits en todos los containers
- ✅ Health checks configurados
- ✅ Backups automáticos de BD

### Opciones de Despliegue

#### Opción 1: VPS (DigitalOcean, AWS EC2, Azure VM)

```bash
# En el servidor
git clone <repo>
cd M2_Proyecto/codigo
cp .env.production .env
docker-compose -f docker-compose.prod.yml up -d

# Configurar reverse proxy (Nginx)
# Configurar SSL (Let's Encrypt)
# Configurar firewall
```

#### Opción 2: Kubernetes (Recomendado para Escala)

Ver documentación de Kubernetes en `docs/kubernetes/`

#### Opción 3: Cloud Managed (AWS ECS, Google Cloud Run, Azure Container Instances)

Configurar deployments automáticos con GitHub Actions.

---

## Checklist de Despliegue

### Pre-Despliegue

- [ ] Variables de entorno configuradas
- [ ] Secrets generados de forma segura
- [ ] Tests unitarios pasando
- [ ] Tests de carga ejecutados
- [ ] Documentación actualizada
- [ ] Backups configurados

### Post-Despliegue

- [ ] Health checks respondiendo
- [ ] Logs sin errores
- [ ] Monitoreo activo
- [ ] Alertas configuradas
- [ ] SSL funcionando
- [ ] Tests de humo exitosos

---

## Siguientes Pasos

Después de un despliegue exitoso:

1. **Monitoreo**: Configurar dashboards de métricas
2. **CI/CD**: Automatizar deployments con GitHub Actions
3. **Backups**: Programar backups diarios de BD
4. **Scaling**: Configurar auto-scaling en producción
5. **Security**: Auditoría de seguridad regular

---

## Soporte y Ayuda

### Recursos

- **Documentación**: [README principal](../README.md)
- **Issues**: [GitHub Issues](https://github.com/D-Araya/fundamentos_arquitectura_cloud/issues)
- **Docker Docs**: https://docs.docker.com
- **FastAPI Docs**: https://fastapi.tiangolo.com

### Contacto

- **GitHub**: [@D-Araya](https://github.com/D-Araya)

---

**Última actualización**: Enero 2026  
**Autor**: Daniel Araya  
**Versión**: 2.0 (Actualizado para Windows/Linux/macOS)