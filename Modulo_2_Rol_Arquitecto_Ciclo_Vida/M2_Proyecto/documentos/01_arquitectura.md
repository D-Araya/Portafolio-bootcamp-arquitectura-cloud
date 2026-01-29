# Arquitectura del Sistema de Reservas

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
3. [Patrones de Diseño](#patrones-de-diseño)
4. [Componentes del Sistema](#componentes-del-sistema)
5. [Flujos de Datos](#flujos-de-datos)
6. [Base de Datos](#base-de-datos)
7. [Seguridad](#seguridad)
8. [Escalabilidad](#escalabilidad)
9. [Diagramas Visuales](#diagramas-visuales)

---

## Visión General

El sistema implementa una **arquitectura de microservicios** basada en contenedores Docker, diseñada para ser escalable, mantenible y resiliente. Cada microservicio es independiente, con su propia lógica de negocio, almacenamiento y ciclo de vida.

### Principios Arquitectónicos

1. **Separation of Concerns**: Cada servicio tiene una responsabilidad única y bien definida
2. **Loose Coupling**: Mínima dependencia entre servicios
3. **High Cohesion**: Funcionalidades relacionadas agrupadas en el mismo servicio
4. **Autonomy**: Cada servicio puede desplegarse independientemente
5. **Resilience**: Diseño tolerante a fallos

---

## Decisiones Arquitectónicas

### 1. Arquitectura de Microservicios

**Decisión**: Implementar microservicios en lugar de monolito

**Justificación**:
- ✅ **Escalabilidad independiente**: Cada servicio escala según su carga específica
- ✅ **Despliegue independiente**: Actualizaciones sin afectar todo el sistema
- ✅ **Tecnología heterogénea**: Flexibilidad para usar diferentes stacks
- ✅ **Equipos autónomos**: Facilita organización de equipos de desarrollo
- ✅ **Aislamiento de fallos**: Un fallo no derriba todo el sistema

**Trade-offs**:
- ⚠️ Mayor complejidad operacional
- ⚠️ Latencia de red entre servicios
- ⚠️ Necesidad de monitoreo distribuido

### 2. API Gateway Pattern

**Decisión**: NGINX como punto de entrada único

**Justificación**:
- ✅ **Punto único de entrada**: Simplifica interacción del cliente
- ✅ **Balanceo de carga**: Distribuye tráfico entre instancias
- ✅ **Rate limiting**: Protección contra abuso
- ✅ **SSL/TLS termination**: Manejo centralizado de certificados
- ✅ **Logging centralizado**: Auditoría de todas las peticiones

### 3. Containerización con Docker

**Decisión**: Docker para todos los servicios

**Justificación**:
- ✅ **Consistencia**: Mismo comportamiento en dev, test y prod
- ✅ **Portabilidad**: Ejecuta en cualquier plataforma
- ✅ **Aislamiento**: Cada servicio en su propio contenedor
- ✅ **Eficiencia**: Menor overhead que VMs
- ✅ **Orquestación**: Fácil escalamiento con Kubernetes futuro

### 4. Base de Datos Compartida (Inicial)

**Decisión**: PostgreSQL compartido entre servicios

**Justificación**:
- ✅ **Simplicidad inicial**: Más fácil de gestionar en MVP
- ✅ **Transacciones ACID**: Consistencia de datos garantizada
- ✅ **Bajo costo**: Un solo servidor de BD
- ✅ **Integridad referencial**: Foreign keys entre entidades

**Nota**: En producción se recomienda migrar a "database per service" pattern.

### 5. Autenticación Stateless con JWT

**Decisión**: JSON Web Tokens para autenticación

**Justificación**:
- ✅ **Stateless**: No requiere almacenar sesiones
- ✅ **Escalable**: Cualquier servicio puede validar tokens
- ✅ **Estándar**: Amplia adopción en la industria
- ✅ **Información en el token**: Claims útiles para autorización

---

## Patrones de Diseño

### 1. API Gateway Pattern

Punto de entrada único que enruta las peticiones a los microservicios correspondientes.

```
Cliente → API Gateway → Microservicio apropiado
```

**Beneficios**:
- Abstrae la complejidad interna
- Reduce roundtrips del cliente
- Centraliza concerns transversales (auth, logging, rate limiting)

### 2. Service Registry Pattern (Implícito)

Docker Compose actúa como service registry mediante DNS interno.

```
gateway → http://auth-service:8000
gateway → http://users-service:8000
```

### 3. Circuit Breaker Pattern (Recomendado para futuro)

Previene cascada de fallos cuando un servicio está caído.

**Estado futuro recomendado**:
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_service():
    # lógica de llamada
```

### 4. Repository Pattern

Abstracción de la capa de datos en cada servicio.

```python
# Ejemplo en reservations-service
class ReservationRepository:
    def create(self, reservation: Reservation) -> Reservation:
        # Lógica de persistencia
    
    def find_by_id(self, id: int) -> Optional[Reservation]:
        # Lógica de consulta
```

### 5. Dependency Injection

Inyección de dependencias para facilitar testing y desacoplamiento.

```python
# FastAPI automáticamente inyecta dependencias
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validación de token
    return user
```

---

## Componentes del Sistema

### Diagrama de Componentes

```
┌────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                │
│                    (Browser / Mobile App)                      │
└─────────────────────────┬──────────────────────────────────────┘
                          │ HTTPS
                          ▼
┌────────────────────────────────────────────────────────────────┐
│                     API GATEWAY (NGINX)                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  - Routing          - Rate Limiting                      │ │
│  │  - Load Balancing   - SSL Termination                    │ │
│  │  - CORS             - Request/Response Logging           │ │
│  └──────────────────────────────────────────────────────────┘ │
└───┬────────────┬────────────┬────────────┬─────────────────────┘
    │            │            │            │
    ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌──────────────┐ ┌─────────┐
│  Auth   │ │  Users  │ │ Reservations │ │ Spaces  │
│ Service │ │ Service │ │   Service    │ │ Service │
└────┬────┘ └────┬────┘ └──────┬───────┘ └────┬────┘
     │           │             │              │
     │           │             │              │
     └───────────┴─────────────┴──────────────┘
                          │
                          ▼
     ┌───────────────────────────────────────┐
     │         CAPA DE PERSISTENCIA          │
     │  ┌─────────────────────────────────┐  │
     │  │      PostgreSQL (Primary)       │  │
     │  │  - users                        │  │
     │  │  - reservations                 │  │
     │  │  - spaces                       │  │
     │  └─────────────────────────────────┘  │
     │  ┌─────────────────────────────────┐  │
     │  │      Redis (Cache)              │  │
     │  │  - Session cache                │  │
     │  │  - Query cache                  │  │
     │  └─────────────────────────────────┘  │
     └───────────────────────────────────────┘
```

### Descripción de Componentes

#### API Gateway (Puerto 80)
**Tecnología**: NGINX  
**Responsabilidades**:
- Enrutamiento de peticiones HTTP
- Balanceo de carga entre instancias
- Rate limiting (100 req/min por IP)
- CORS configurado para seguridad
- Logs de acceso centralizados

**Configuración clave**:
```nginx
upstream auth_service {
    server auth-service:8000;
}

location /api/auth {
    proxy_pass http://auth_service;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

#### Auth Service (Puerto 8001)
**Tecnología**: FastAPI + Python 3.11  
**Responsabilidades**:
- Registro de usuarios
- Autenticación (login)
- Emisión y validación de JWT tokens
- Gestión de sesiones

**Endpoints principales**:
- `POST /auth/register` - Crear nueva cuenta
- `POST /auth/login` - Obtener token JWT
- `POST /auth/refresh` - Renovar token
- `POST /auth/validate` - Validar token (uso interno)

#### Users Service (Puerto 8002)
**Tecnología**: FastAPI + Python 3.11  
**Responsabilidades**:
- CRUD de perfiles de usuario
- Actualización de información personal
- Gestión de preferencias
- Eliminación de cuentas

**Endpoints principales**:
- `GET /users/me` - Perfil del usuario actual
- `PUT /users/me` - Actualizar perfil
- `DELETE /users/me` - Eliminar cuenta
- `GET /users/{id}` - Obtener usuario (admin)

#### Reservations Service (Puerto 8003)
**Tecnología**: FastAPI + Python 3.11  
**Responsabilidades**:
- Crear nuevas reservas
- Consultar reservas existentes
- Cancelar reservas
- Validar disponibilidad
- Aplicar reglas de negocio

**Endpoints principales**:
- `POST /reservations` - Nueva reserva
- `GET /reservations` - Listar reservas del usuario
- `GET /reservations/{id}` - Detalle de reserva
- `DELETE /reservations/{id}` - Cancelar reserva
- `GET /reservations/search` - Búsqueda avanzada

**Lógica de negocio**:
- Validación de conflictos de horario
- Verificación de capacidad del espacio
- Cálculo de duración y costo
- Notificaciones (futuro)

#### Spaces Service (Puerto 8004)
**Tecnología**: FastAPI + Python 3.11  
**Responsabilidades**:
- CRUD de espacios reservables
- Consulta de disponibilidad
- Gestión de capacidades
- Metadata de espacios

**Endpoints principales**:
- `GET /spaces` - Listar espacios disponibles
- `GET /spaces/{id}` - Detalle de espacio
- `GET /spaces/{id}/availability` - Verificar disponibilidad
- `POST /spaces` - Crear espacio (admin)
- `PUT /spaces/{id}` - Actualizar espacio (admin)

---

## Flujos de Datos

### Flujo 1: Registro de Usuario

```
Cliente                Gateway             Auth Service          Database
  |                      |                      |                    |
  |--Register Request--->|                      |                    |
  |                      |---Forward Request--->|                    |
  |                      |                      |--Validate Data-    |
  |                      |                      |--Hash Password     |
  |                      |                      |---Insert User----->|
  |                      |                      |<---User Created----|
  |                      |                      |--Generate JWT-     |
  |                      |<--Return JWT---------|                    |
  |<--Success + Token----|                      |                    |
```

### Flujo 2: Login

```
Cliente                Gateway             Auth Service          Database
  |                      |                      |                    |
  |--Login Credentials-->|                      |                    |
  |                      |---Forward Request--->|                    |
  |                      |                      |---Query User------>|
  |                      |                      |<--User Data--------|
  |                      |                      |--Verify Password   |
  |                      |                      |--Generate JWT-     |
  |                      |<--Return JWT---------|                    |
  |<--Success + Token----|                      |                    |
```

### Flujo 3: Crear Reserva (Autenticado)

```
Cliente          Gateway      Auth Service    Reservations     Spaces      Database
  |                |                |               |             |            |
  |--POST /reservations + JWT-->    |               |             |            |
  |                |-----Validate JWT-------------->|             |            |
  |                |<---Valid User ID---------------|             |            |
  |                |-----Forward Request----------->|             |            |
  |                |                                |--Check Space Avail.----->|
  |                |                                |<---Space Details---------|
  |                |                                |--Validate Rules-          |
  |                |                                |---Create Reservation---->|
  |                |                                |<---Reservation Created---|
  |                |<---Return Reservation---------|             |            |
  |<--Success + Reservation ID-|                   |             |            |
```

### Flujo 4: Consultar Disponibilidad

```
Cliente          Gateway         Spaces Service      Database
  |                |                    |                |
  |--GET /spaces/1/availability?date=-->|                |
  |                |----Forward--------->|                |
  |                |                     |--Query Reservations-->
  |                |                     |<--Reservations--|
  |                |                     |--Calculate Slots-
  |                |<--Available Slots---|                |
  |<--Availability-|                     |                |
```

---

## Base de Datos

### Modelo Entidad-Relación

```
┌─────────────────────┐
│       USERS         │
├─────────────────────┤
│ id (PK)            │
│ email (UNIQUE)      │
│ password_hash       │
│ name                │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1
           │
           │ *
┌──────────┴──────────┐         ┌─────────────────────┐
│   RESERVATIONS      │    *    │       SPACES        │
├─────────────────────┤  ◄────  ├─────────────────────┤
│ id (PK)            │    1    │ id (PK)            │
│ user_id (FK)       │         │ name                │
│ space_id (FK)      │─────────│ description         │
│ start_time         │         │ capacity            │
│ end_time           │         │ location            │
│ status             │         │ amenities (JSON)    │
│ created_at         │         │ created_at          │
│ updated_at         │         │ updated_at          │
└────────────────────┘         └─────────────────────┘
```

### Esquema SQL

```sql
-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Tabla de espacios
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    capacity INTEGER NOT NULL,
    location VARCHAR(255),
    amenities JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_spaces_active ON spaces(is_active);

-- Tabla de reservas
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    space_id INTEGER NOT NULL REFERENCES spaces(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_time_range CHECK (end_time > start_time),
    CONSTRAINT valid_status CHECK (status IN ('active', 'cancelled', 'completed'))
);

CREATE INDEX idx_reservations_user ON reservations(user_id);
CREATE INDEX idx_reservations_space ON reservations(space_id);
CREATE INDEX idx_reservations_time ON reservations(start_time, end_time);
CREATE INDEX idx_reservations_status ON reservations(status);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spaces_updated_at BEFORE UPDATE ON spaces
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reservations_updated_at BEFORE UPDATE ON reservations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Estrategia de Caché (Redis)

```
# Patrón de caching para consultas frecuentes
Key Pattern: {service}:{entity}:{id}:{operation}

Ejemplos:
- spaces:list:all             TTL: 5 min
- spaces:1:details            TTL: 10 min
- spaces:1:availability       TTL: 1 min
- reservations:user:123       TTL: 2 min
```

---

## Seguridad

### 1. Autenticación y Autorización

**JWT Token Structure**:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@example.com",
    "role": "user",
    "exp": 1735689600,
    "iat": 1735603200
  }
}
```

**Token Lifecycle**:
- **Duración**: 24 horas
- **Refresh**: Endpoint `/auth/refresh` antes de expiración
- **Revocación**: Blacklist en Redis (futuro)

### 2. Protección de Datos

| Dato | Medida de Seguridad |
|------|---------------------|
| Passwords | Bcrypt hash (factor 12) |
| JWT | Firmado con secret key |
| Datos en tránsito | HTTPS (TLS 1.3 ready) |
| Variables sensibles | Environment variables |
| Database credentials | Docker secrets |

### 3. Rate Limiting

```nginx
# En NGINX Gateway
limit_req_zone $binary_remote_addr zone=general:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/m;

location /api/auth {
    limit_req zone=auth burst=5;
}

location /api/ {
    limit_req zone=general burst=20;
}
```

### 4. Input Validation

```python
# Ejemplo con Pydantic en FastAPI
from pydantic import BaseModel, EmailStr, constr, validator

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    name: constr(min_length=2, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Must contain digit')
        return v
```

### 5. CORS Configuration

```python
# FastAPI CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # En prod: dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## Escalabilidad

### Escalamiento Horizontal

**Capacidad actual con Docker Compose**:
```yaml
# docker-compose.yml
services:
  auth-service:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

**Escalamiento manual**:
```bash
docker-compose up -d --scale auth-service=3
docker-compose up -d --scale reservations-service=5
```

### Puntos de Escalamiento

| Servicio | Bottleneck Esperado | Estrategia de Escalamiento |
|----------|---------------------|----------------------------|
| Auth Service | Login en horas pico | Horizontal + Cache de sesiones |
| Users Service | Consultas de perfil | Horizontal + Read replicas |
| Reservations Service | Creación concurrente | Horizontal + Queue pattern |
| Spaces Service | Consultas de disponibilidad | Horizontal + Aggressive caching |

### Futuro: Kubernetes

**Horizontal Pod Autoscaler**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: reservations-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: reservations-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Database Scaling

**Actual**: Single PostgreSQL instance

**Mejoras futuras**:
1. **Read Replicas**: Para queries de lectura
2. **Connection Pooling**: PgBouncer
3. **Sharding**: Por tenant_id o region
4. **Database per Service**: Independencia total

---

## Resiliencia y Alta Disponibilidad

### Health Checks

Todos los servicios exponen `/health`:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "reservations-service",
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Graceful Shutdown

```python
# Signal handling para shutdown limpio
import signal
import sys

def signal_handler(sig, frame):
    logger.info("Shutting down gracefully...")
    # Completar requests en proceso
    # Cerrar conexiones a BD
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

### Retry Logic (Recomendado)

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_external_service():
    # Lógica con retry automático
    pass
```

---

## Próximos Pasos Arquitectónicos

### Corto Plazo
1. ✅ Implementar Circuit Breaker pattern
2. ✅ Agregar observabilidad (Prometheus + Grafana)
3. ✅ Implementar logging estructurado (ELK Stack)
4. ✅ Distributed tracing (Jaeger)

### Mediano Plazo
5. ✅ Migrar a Kubernetes
6. ✅ Implementar Service Mesh (Istio/Linkerd)
7. ✅ Database per service
8. ✅ Event-driven architecture (Kafka/RabbitMQ)

### Largo Plazo
9. ✅ Multi-region deployment
10. ✅ CQRS pattern para queries complejas
11. ✅ Machine Learning para recomendaciones
12. ✅ GraphQL API adicional

---

## Diagramas Visuales

### Arquitectura del Sistema

![Arquitectura del Sistema](../imagenes/arquitectura_sistema.png)

*Vista general de la arquitectura de microservicios con API Gateway, 4 servicios backend (Auth, Users, Reservations, Spaces) y capa de persistencia (PostgreSQL + Redis). Muestra el flujo de comunicación desde el cliente hasta la base de datos.*

### Modelo de Datos

![Diagrama Entidad-Relación](../imagenes/diagrama_er.png)

*Modelo de base de datos mostrando las relaciones entre las entidades Users, Spaces y Reservations con sus atributos, tipos de datos, claves primarias, claves foráneas y constraints. Incluye las cardinalidades de las relaciones (1:N entre Users-Reservations y Spaces-Reservations).*

### Flujo de Operación

![Diagrama de Secuencia](../imagenes/diagrama_secuencia.png)

*Secuencia detallada de interacciones para crear una reserva. Muestra el flujo completo desde la petición del cliente, pasando por la validación de JWT en Auth Service, verificación de disponibilidad con Spaces Service, creación de la reserva en Reservations Service, y persistencia en PostgreSQL. Incluye tiempos aproximados y manejo de respuestas.*

---

## Conclusiones

Esta arquitectura proporciona una base sólida para un sistema de reservas escalable y mantenible. Los principios de microservicios, containerización y diseño stateless permiten que el sistema crezca según las necesidades del negocio.

**Fortalezas**:
- ✅ Escalabilidad demostrada
- ✅ Despliegue independiente de servicios
- ✅ Aislamiento de fallos
- ✅ Flexibilidad tecnológica

**Áreas de Mejora**:
- ⚠️ Implementar observabilidad completa
- ⚠️ Agregar resiliencia con circuit breakers
- ⚠️ Migrar a database per service
- ⚠️ Implementar event-driven patterns

---

**Última actualización**: Enero 2026  
**Autor**: Daniel Araya  
**Versión**: 2.0 (Con diagramas visuales)