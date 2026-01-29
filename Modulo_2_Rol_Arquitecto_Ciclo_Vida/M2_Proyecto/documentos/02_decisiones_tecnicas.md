# Decisiones Técnicas del Proyecto

## 📋 Índice

1. [Stack Tecnológico](#stack-tecnológico)
2. [Justificación de Tecnologías](#justificación-de-tecnologías)
3. [Alternativas Evaluadas](#alternativas-evaluadas)
4. [Trade-offs y Compromisos](#trade-offs-y-compromisos)
5. [Decisiones de Diseño](#decisiones-de-diseño)
6. [Herramientas de Desarrollo](#herramientas-de-desarrollo)

---

## Stack Tecnológico

### Resumen

| Capa | Tecnología | Versión | Justificación |
|------|------------|---------|---------------|
| **API Gateway** | NGINX | 1.25 | Rendimiento, estabilidad, simplicidad |
| **Backend** | FastAPI | 0.109+ | Async, tipado, documentación automática |
| **Lenguaje** | Python | 3.11+ | Productividad, ecosistema, legibilidad |
| **Base de Datos** | PostgreSQL | 15+ | ACID, robustez, comunidad |
| **Caché** | Redis | 7+ | Velocidad, versatilidad, simplicidad |
| **Containerización** | Docker | 24+ | Estándar de industria, portabilidad |
| **Orquestación** | Docker Compose | 2.24+ | Simplicidad para desarrollo local |
| **Testing** | pytest | 8+ | Framework maduro, plugins extensos |
| **Load Testing** | k6 | 0.48+ | Performance, scripting en JS |

---

## Justificación de Tecnologías

### 1. Backend: FastAPI + Python

#### ¿Por qué FastAPI?

**Ventajas**:
- ✅ **Alto Rendimiento**: Comparable a Node.js y Go gracias a Starlette y Pydantic
- ✅ **Async/Await Nativo**: Manejo eficiente de I/O concurrente
- ✅ **Documentación Automática**: OpenAPI (Swagger) y ReDoc out-of-the-box
- ✅ **Validación de Datos**: Pydantic para validación automática de tipos
- ✅ **Type Hints**: Código más seguro y mantenible
- ✅ **Dependency Injection**: Sistema elegante de DI integrado
- ✅ **Comunidad Activa**: Rápido crecimiento, buena documentación

**Código de ejemplo**:
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

@app.post("/users")
async def create_user(user: UserCreate):
    # Validación automática por Pydantic
    # Documentación automática generada
    return {"id": 1, "email": user.email}
```

**Alternativas consideradas**:
- Flask: Más maduro pero síncrono, requiere más boilerplate
- Django REST Framework: Demasiado pesado para microservicios
- Express (Node.js): Buen rendimiento pero menor productividad
- Spring Boot (Java): Excelente pero verbose, mayor curva de aprendizaje

#### ¿Por qué Python?

**Ventajas**:
- ✅ **Productividad**: Desarrollo rápido, sintaxis clara
- ✅ **Ecosistema Rico**: Millones de librerías disponibles
- ✅ **Comunidad**: Enorme comunidad, abundante documentación
- ✅ **Machine Learning Ready**: Facilita integraciones futuras (scikit-learn, TensorFlow)
- ✅ **DevOps**: Excelente tooling (black, mypy, ruff)

**Desventajas aceptadas**:
- ⚠️ No es el lenguaje más rápido (pero FastAPI compensa)
- ⚠️ GIL para CPU-bound tasks (no aplica en I/O-bound como APIs)

---

### 2. Base de Datos: PostgreSQL

#### ¿Por qué PostgreSQL?

**Ventajas**:
- ✅ **ACID Compliant**: Garantías de transacciones
- ✅ **Robustez**: Probado en producción por décadas
- ✅ **Características Avanzadas**: JSON, Full-text search, GIS
- ✅ **Open Source**: Sin costos de licenciamiento
- ✅ **Rendimiento**: Excelente para read-heavy workloads
- ✅ **Extensible**: Soporte para extensiones (PostGIS, pg_trgm)
- ✅ **Comunidad**: Documentación excepcional

**Características utilizadas**:
```sql
-- JSONB para flexibilidad
CREATE TABLE spaces (
    amenities JSONB  -- Almacenamiento flexible de características
);

-- Índices para performance
CREATE INDEX idx_reservations_time ON reservations(start_time, end_time);

-- Constraints para integridad
CONSTRAINT valid_time_range CHECK (end_time > start_time)
```

**Alternativas consideradas**:
- MySQL: Menos features avanzadas, pero también válido
- MongoDB: NoSQL flexible pero perdemos ACID y joins
- SQLite: Muy limitado para producción

**Decisión**: PostgreSQL por su balance entre features y rendimiento.

---

### 3. Caché: Redis

#### ¿Por qué Redis?

**Ventajas**:
- ✅ **Velocidad Extrema**: Operaciones en memoria, latencia sub-milisegundo
- ✅ **Versatilidad**: Cache, sessions, pub/sub, queues
- ✅ **Estructuras de Datos**: Strings, hashes, lists, sets, sorted sets
- ✅ **Persistencia Opcional**: RDB snapshots o AOF
- ✅ **Simplicidad**: API sencilla, fácil de usar

**Casos de uso en el proyecto**:

1. **Query Caching**:
```python
# Ejemplo de caching
import redis
r = redis.Redis()

def get_spaces():
    cached = r.get("spaces:list")
    if cached:
        return json.loads(cached)
    
    spaces = db.query(Space).all()
    r.setex("spaces:list", 300, json.dumps(spaces))  # TTL 5 min
    return spaces
```

2. **Session Store**: Almacenar tokens invalidados (blacklist)
3. **Rate Limiting**: Contadores de requests por IP

**Alternativas consideradas**:
- Memcached: Más simple pero menos features
- In-memory (sin caché): Performance insuficiente

---

### 4. API Gateway: NGINX

#### ¿Por qué NGINX?

**Ventajas**:
- ✅ **Rendimiento**: Maneja 10,000+ conexiones concurrentes
- ✅ **Bajo Consumo**: Footprint mínimo de memoria
- ✅ **Estabilidad**: Extremadamente confiable
- ✅ **Features**: Load balancing, SSL, rate limiting, caching
- ✅ **Configuración Declarativa**: Archivos de config simples

**Configuración clave**:
```nginx
# Load balancing con health checks
upstream reservations {
    least_conn;  # Algoritmo de balanceo
    server reservations-service:8000 max_fails=3 fail_timeout=30s;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://reservations;
}
```

**Alternativas consideradas**:
- Kong: Más features pero más complejo, requiere BD
- Traefik: Excelente para Kubernetes, overkill para Docker Compose
- AWS API Gateway: Cloud-specific, evitamos vendor lock-in
- Envoy: Moderno pero curva de aprendizaje pronunciada

**Decisión**: NGINX por su simplicidad, rendimiento y madurez.

---

### 5. Containerización: Docker

#### ¿Por qué Docker?

**Ventajas**:
- ✅ **Consistencia**: "Works on my machine" solved
- ✅ **Portabilidad**: Mismo container en dev, test, prod
- ✅ **Aislamiento**: Dependencias independientes por servicio
- ✅ **Eficiencia**: Menor overhead que VMs
- ✅ **Ecosistema**: Docker Hub, registries, herramientas

**Dockerfile ejemplo**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la aplicación
COPY . .

# Usuario no-root por seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Best practices aplicadas**:
- Multi-stage builds para imágenes ligeras
- Usuario no-root por seguridad
- Layer caching optimization
- .dockerignore para excluir archivos innecesarios

---

### 6. Orquestación: Docker Compose

#### ¿Por qué Docker Compose?

**Ventajas**:
- ✅ **Simplicidad**: Perfecto para desarrollo y testing local
- ✅ **Declarativo**: Infraestructura como código (YAML)
- ✅ **Rápido**: Setup en segundos con `docker-compose up`
- ✅ **Networking**: Automático entre servicios
- ✅ **Volumes**: Persistencia de datos fácil

**docker-compose.yml ejemplo**:
```yaml
version: '3.9'

services:
  gateway:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
    volumes:
      - ./gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - auth-service
      - users-service
      - reservations-service
    networks:
      - app-network

  auth-service:
    build: ./auth-service
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/reservations
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - postgres
      - redis
    networks:
      - app-network
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=reservations_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=reservations
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
```

**Para producción**: Kubernetes o ECS reemplazaría Docker Compose.

---

### 7. Testing: pytest + k6

#### pytest para Tests Unitarios

**Ventajas**:
- ✅ **Pythonic**: Sintaxis natural de Python
- ✅ **Fixtures**: Dependency injection para tests
- ✅ **Plugins**: Enorme ecosistema (pytest-asyncio, pytest-cov)
- ✅ **Assertions**: Mensajes de error claros y útiles

**Ejemplo de test**:
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "Test123!"
    })
    return response.json()["access_token"]

def test_create_reservation(auth_token):
    response = client.post(
        "/reservations",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "space_id": 1,
            "start_time": "2026-01-20T10:00:00",
            "end_time": "2026-01-20T12:00:00"
        }
    )
    assert response.status_code == 201
    assert "id" in response.json()
```

#### k6 para Load Testing

**Ventajas**:
- ✅ **Performance**: Escrito en Go, maneja alta carga
- ✅ **Developer-friendly**: Scripts en JavaScript
- ✅ **Métricas**: Reportes detallados y visualizables
- ✅ **CI/CD Ready**: Fácil integración

**Script de carga**:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // Ramp up
    { duration: '1m', target: 100 },   // Stay at 100 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],  // 95% bajo 200ms
  },
};

export default function () {
  const res = http.get('http://localhost/api/spaces');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
```

**Alternativas**:
- JMeter: Más features pero GUI pesada, XML verbose
- Locust: Python, buen para scenarios complejos
- Artillery: Node.js, similar a k6

---

## Alternativas Evaluadas

### Backend Framework

| Framework | Pros | Contras | Decisión |
|-----------|------|---------|----------|
| **FastAPI** ✅ | Async, rápido, tipos, docs automáticas | Relativamente nuevo | **Elegido** |
| Flask | Maduro, simple, flexible | Síncrono, mucho boilerplate | No |
| Django REST | Full-featured, admin, ORM | Monolítico, pesado para microservicios | No |
| Express.js | Rápido, ecosistema Node | Callback hell, menos productivo | No |
| Spring Boot | Robusto, empresarial | Verbose, pesado, curva aprendizaje | No |

### Base de Datos

| DB | Pros | Contras | Decisión |
|----|------|---------|----------|
| **PostgreSQL** ✅ | ACID, features avanzadas, JSON | Horizontal scaling complejo | **Elegido** |
| MySQL | Popular, simple | Menos features avanzadas | No |
| MongoDB | Flexible schema, escala horizontal | Sin ACID multi-doc (antes), joins limitados | No |
| DynamoDB | Serverless, escala automática | Vendor lock-in, costo | No |

### API Gateway

| Gateway | Pros | Contras | Decisión |
|---------|------|---------|----------|
| **NGINX** ✅ | Rápido, estable, simple | Configuración estática | **Elegido** |
| Kong | Plugin ecosystem, features | Requiere BD, más complejo | No |
| Traefik | Kubernetes-native, dinámico | Overkill para Compose | No |
| API Gateway (AWS/GCP) | Managed, escala automática | Vendor lock-in, costo | No |

---

## Trade-offs y Compromisos

### 1. Base de Datos Compartida vs. Database per Service

**Decisión**: BD compartida (PostgreSQL única)

**Pros**:
- ✅ Simplicidad de gestión
- ✅ Transacciones ACID entre entidades
- ✅ Menor costo de infraestructura
- ✅ Setup rápido para MVP

**Contras**:
- ⚠️ Acoplamiento a nivel de datos
- ⚠️ Punto único de fallo
- ⚠️ Dificulta escalamiento independiente
- ⚠️ Schema changes afectan múltiples servicios

**Justificación**: Para un MVP y ambiente de desarrollo, la simplicidad supera las desventajas. En producción se recomienda migrar a database-per-service.

**Plan de migración futuro**:
```
Fase 1 (actual): Shared PostgreSQL
         ↓
Fase 2: Replication + Read replicas por servicio
         ↓
Fase 3: Database per service + Event-driven sync
```

### 2. Síncrono vs. Asíncrono (Event-Driven)

**Decisión**: Comunicación síncrona HTTP/REST

**Pros**:
- ✅ Simplicidad
- ✅ Debugging más fácil
- ✅ Menos infraestructura (no message broker)
- ✅ Request-response familiar

**Contras**:
- ⚠️ Acoplamiento temporal
- ⚠️ Sin retry automático
- ⚠️ Fallos en cascada posibles

**Justificación**: Para workflows simples de crear/consultar/cancelar reservas, REST es suficiente y más simple.

**Cuándo migrar a eventos**:
- Workflows complejos multi-step
- Necesidad de garantías de entrega
- Procesamiento asíncrono de larga duración
- Desacoplamiento temporal crítico

### 3. Docker Compose vs. Kubernetes

**Decisión**: Docker Compose para desarrollo

**Pros**:
- ✅ Setup extremadamente rápido
- ✅ Curva de aprendizaje baja
- ✅ Perfecto para desarrollo local
- ✅ Menos recursos consumidos

**Contras**:
- ⚠️ No es para producción
- ⚠️ Sin auto-healing
- ⚠️ Escalamiento manual
- ⚠️ Sin rolling updates

**Justificación**: El proyecto es educativo y para portafolio. Kubernetes sería over-engineering en este contexto.

**Path to production**:
```bash
Development: Docker Compose
     ↓
Staging: Docker Swarm (opcional)
     ↓
Production: Kubernetes (EKS, GKE, AKS)
```

### 4. Monolito vs. Microservicios

**Decisión**: Microservicios

**Pros**:
- ✅ Escalamiento independiente
- ✅ Deploy independiente
- ✅ Aislamiento de fallos
- ✅ Tecnología heterogénea posible
- ✅ Aprendizaje de arquitectura cloud

**Contras**:
- ⚠️ Complejidad operacional
- ⚠️ Latencia entre servicios
- ⚠️ Debugging distribuido más difícil
- ⚠️ Transacciones distribuidas complejas

**Justificación**: El objetivo educativo es aprender arquitectura cloud y microservicios. Los beneficios de aprendizaje justifican la complejidad adicional.

---

## Decisiones de Diseño

### 1. Stateless Services

**Decisión**: Todos los servicios son stateless

**Implementación**:
- JWT para autenticación (no sesiones en servidor)
- Estado persistido en BD
- Cache en Redis (no en memoria del proceso)

**Beneficios**:
- Escalamiento horizontal simple
- Reinicio de containers sin pérdida de estado
- Load balancing round-robin funciona

### 2. API-First Design

**Decisión**: OpenAPI specs generadas automáticamente

**Implementación**:
```python
# FastAPI genera automáticamente:
# - /docs (Swagger UI)
# - /redoc (ReDoc)
# - /openapi.json (Spec)
```

**Beneficios**:
- Documentación siempre actualizada
- Client SDKs auto-generables
- Contract testing facilitado

### 3. Error Handling Consistency

**Decisión**: Formato estándar de errores

**Implementación**:
```python
# Formato de error consistente
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "email",
                "issue": "Invalid email format"
            }
        ],
        "timestamp": "2026-01-19T10:30:00Z",
        "request_id": "req-123-abc"
    }
}
```

### 4. Versioning Strategy

**Decisión**: URL versioning (v1, v2)

**Implementación**:
```python
@app.get("/api/v1/reservations")
async def list_reservations_v1():
    # Versión 1

@app.get("/api/v2/reservations")
async def list_reservations_v2():
    # Versión 2 con breaking changes
```

**Alternativas descartadas**:
- Header versioning: Menos visible
- Content negotiation: Más complejo

---

## Herramientas de Desarrollo

### Code Quality

| Herramienta | Propósito | Configuración |
|-------------|-----------|---------------|
| **black** | Code formatter | `line-length = 100` |
| **ruff** | Linter (reemplazo de flake8) | `select = ["E", "F", "I"]` |
| **mypy** | Type checker | `strict = true` |
| **isort** | Import sorting | Integrado en ruff |

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

### Development Environment

```bash
# pyproject.toml
[tool.poetry]
name = "reservations-service"
version = "1.0.0"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}
sqlalchemy = "^2.0.25"
pydantic = "^2.5.3"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
psycopg2-binary = "^2.9.9"
redis = "^5.0.1"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.4"
pytest-asyncio = "^0.23.3"
pytest-cov = "^4.1.0"
httpx = "^0.26.0"
faker = "^22.0.0"
```

---

## Conclusiones

Las decisiones técnicas tomadas balance an:

1. **Simplicidad vs. Robustez**: Suficientemente simple para desarrollo rápido, suficientemente robusto para demostrar patrones profesionales

2. **Aprendizaje vs. Producción**: Optimizado para aprendizaje de arquitectura cloud, pero con path claro a producción

3. **Costo vs. Features**: Stack open-source minimiza costos mientras proporciona features enterprise-grade

4. **Presente vs. Futuro**: Arquitectura actual funcional, con roadmap claro hacia mejoras (Kubernetes, service mesh, etc.)

### Principales Fortalezas

- ✅ Stack moderno y en demanda en la industria
- ✅ Alta productividad de desarrollo
- ✅ Excelente documentación de todas las tecnologías
- ✅ Path claro de escalamiento
- ✅ Best practices de la industria aplicadas

### Áreas de Mejora Futuras

- Migrar a database-per-service
- Implementar message broker (Kafka/RabbitMQ)
- Agregar observabilidad completa (Prometheus, Grafana, Jaeger)
- Deploy en Kubernetes con CI/CD

---

**Última actualización**: Enero 2026  
**Autor**: Daniel Araya  
**Versión**: 1.0