# Sistema de Reservas en la Nube - Arquitectura de Microservicios

![Estado del Proyecto](https://img.shields.io/badge/estado-completado-success)
![Licencia](https://img.shields.io/badge/licencia-MIT-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Tests](https://img.shields.io/badge/tests-87%2F87%20passing-success)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

## 📌 Descripción

Sistema de reservas escalable basado en arquitectura de microservicios, diseñado para gestionar reservas de espacios y recursos con alta disponibilidad, seguridad y rendimiento óptimo. Este proyecto demuestra la implementación profesional de los pilares fundamentales de la arquitectura cloud.

### 🎯 Características Principales

- ✅ **Arquitectura de Microservicios**: 4 servicios independientes y desacoplados
- ✅ **Escalabilidad Horizontal**: Preparado para auto-scaling
- ✅ **Seguridad Integrada**: JWT + bcrypt + validaciones robustas
- ✅ **Alto Rendimiento**: p95 < 200ms en tests de carga
- ✅ **Containerización Completa**: Docker + Docker Compose
- ✅ **Testing Completo**: 87 tests implementados, 90% cobertura
- ✅ **Documentación Profesional**: Lista para portafolio

---

## 🏗️ Arquitectura del Sistema

### Diagrama Visual

![Arquitectura del Sistema](./imagenes/arquitectura_sistema.png)

*Figura 1: Arquitectura de microservicios con API Gateway, 4 servicios backend y capa de persistencia*

### Visión General (Texto)

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────┐
│      API Gateway (NGINX)            │
│  • Enrutamiento a microservicios    │
│  • Load Balancing                   │
│  • Rate Limiting (100 req/min)      │
│  • CORS configurado                 │
└──────┬──────────────────────────────┘
       │
       ├─────────────┬─────────────┬─────────────┐
       ▼             ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Auth      │ │   Users     │ │ Reservations│ │   Spaces    │
│  Service    │ │  Service    │ │   Service   │ │   Service   │
│ Port: 8001  │ │ Port: 8002  │ │ Port: 8003  │ │ Port: 8004  │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │
       └───────────────┴───────────────┴───────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   PostgreSQL 15  │
                    │   + Redis 7      │
                    └──────────────────┘
```

### Modelo de Datos

![Diagrama Entidad-Relación](./imagenes/diagrama_er.png)

*Figura 2: Modelo de base de datos con relaciones entre Users, Spaces y Reservations*

### Flujo de Reserva

![Diagrama de Secuencia](./imagenes/diagrama_secuencia.png)

*Figura 3: Secuencia de interacciones para crear una reserva con validación de disponibilidad*

**Documentación detallada**: [Ver Arquitectura Completa](./documentos/01_arquitectura.md)

---

## 🚀 Inicio Rápido (Windows)

### Prerequisitos

- **Docker Desktop** >= 20.10 ([Descargar](https://www.docker.com/products/docker-desktop))
- **Git** ([Descargar](https://git-scm.com/download/win))
- **WSL 2** (recomendado para mejor performance)

### Instalación en 5 Pasos

```powershell
# 1. Clonar repositorio
git clone https://github.com/D-Araya/fundamentos_arquitectura_cloud.git
cd fundamentos_arquitectura_cloud\Modulo_2_Rol_Arquitecto_Ciclo_Vida\M2_Proyecto

# 2. Navegar a código
cd codigo

# 3. Configurar variables de entorno
copy .env.example .env
notepad .env  # Editar JWT_SECRET y POSTGRES_PASSWORD

# 4. Levantar servicios
docker-compose up -d

# 5. Verificar que todo funciona
curl http://localhost/health
```

### Verificación Completa

```powershell
# Health checks de todos los servicios
curl http://localhost/api/auth/health
curl http://localhost/api/users/health
curl http://localhost/api/reservations/health
curl http://localhost/api/spaces/health
```

**Si todos responden `"status": "healthy"` ✅ ¡Sistema operativo!**

---

## 📖 Documentación

### Documentos Principales

| Documento | Descripción | Link |
|-----------|-------------|------|
| **Consigna** | Requerimientos reformulados profesionalmente | [Ver](./documentos/CONSIGNA_REFORMULADA.md) |
| **Arquitectura** | Diseño completo, patrones, decisiones | [Ver](./documentos/01_arquitectura.md) |
| **Decisiones Técnicas** | Justificación de tecnologías elegidas | [Ver](./documentos/02_decisiones_tecnicas.md) |
| **Guía de Despliegue** | Instalación paso a paso + troubleshooting | [Ver](./documentos/03_guia_despliegue.md) |
| **Informe de Pruebas** | Tests reales implementados y ejecutables | [Ver](./documentos/04_informe_pruebas.md) |

---

## 💻 Código Fuente

### Estructura del Proyecto

```
M2_Proyecto/
├── README.md                         ← Este archivo
│
├── documentos/                       ← Documentación técnica completa
│   ├── CONSIGNA_REFORMULADA.md
│   ├── 01_arquitectura.md
│   ├── 02_decisiones_tecnicas.md
│   ├── 03_guia_despliegue.md
│   └── 04_informe_pruebas.md
│
├── imagenes/                         ← Diagramas del sistema
│   ├── arquitectura_sistema.png     ✅
│   ├── diagrama_er.png               ✅
│   └── diagrama_secuencia.png        ✅
│
├── codigo/                           ← Código fuente completo
│   ├── README.md                     ← Guía de ejecución
│   ├── docker-compose.yml            ← Orquestación
│   ├── .env.example                  ← Template configuración
│   │
│   ├── gateway/                      ← NGINX API Gateway
│   │   └── nginx.conf
│   │
│   ├── database/                     ← Scripts PostgreSQL
│   │   ├── init.sql                  ← Schema + triggers
│   │   └── seed.sql                  ← Datos de prueba
│   │
│   ├── auth-service/                 ← Autenticación JWT
│   │   ├── main.py                   ← 320 líneas
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   │       └── test_auth.py          ← 23 tests ✅
│   │
│   ├── users-service/                ← Gestión de usuarios
│   │   ├── main.py                   ← 250 líneas
│   │   ├── tests/test_users.py       ← 18 tests ✅
│   │   └── ...
│   │
│   ├── reservations-service/         ← CRUD reservas
│   │   ├── main.py                   ← 400 líneas
│   │   ├── tests/test_reservations.py ← 28 tests ✅
│   │   └── ...
│   │
│   └── spaces-service/               ← Gestión espacios
│       ├── main.py                   ← 350 líneas
│       ├── tests/test_spaces.py      ← 18 tests ✅
│       └── ...
│
└── tests/                            ← Tests de sistema
    ├── README.md                     ← Guía de testing
    └── load/
        └── sustained-load.js         ← Pruebas k6 ✅
```

**Guía detallada**: [Ver README de Código](./codigo/README.md)

---

## 🧪 Testing

### Tests Implementados

| Servicio | Tests | Cobertura | Estado |
|----------|-------|-----------|--------|
| **Auth Service** | 23 | 93% | ✅ Implementado |
| **Users Service** | 18 | 92% | ✅ Implementado |
| **Reservations Service** | 28 | 88% | ✅ Implementado |
| **Spaces Service** | 18 | 87% | ✅ Implementado |
| **TOTAL** | **87** | **90%** | ✅ **100% Completo** |

### Ejecutar Tests

```powershell
# Desde codigo/
cd codigo

# Tests individuales
docker-compose exec auth-service pytest -v
docker-compose exec users-service pytest -v
docker-compose exec reservations-service pytest -v
docker-compose exec spaces-service pytest -v

# Con cobertura HTML
docker-compose exec auth-service pytest --cov=main --cov-report=html
docker-compose exec users-service pytest --cov=main --cov-report=html
docker-compose exec reservations-service pytest --cov=main --cov-report=html
docker-compose exec spaces-service pytest --cov=main --cov-report=html
```

**Guía completa**: [Ver Informe de Pruebas](./documentos/04_informe_pruebas.md)

---

## 🔒 Seguridad

### Características Implementadas

- ✅ **JWT Tokens**: HS256, expiración 24h, refresh incluido
- ✅ **Password Hashing**: bcrypt factor 12
- ✅ **Input Validation**: Pydantic con validators custom
- ✅ **Rate Limiting**: 100 req/min general, 10 req/min auth
- ✅ **CORS**: Configurado en todos los servicios
- ✅ **SQL Injection Prevention**: SQLAlchemy ORM

### Credenciales de Desarrollo

```
Email: admin@reservations.com
Password: Test123!
Rol: Administrador
```

**⚠️ Solo para desarrollo - Eliminar en producción**

---

## 📊 APIs Disponibles

### Endpoints Principales

#### Autenticación (`/api/auth`)
- `POST /register` - Registrar usuario
- `POST /login` - Obtener token JWT
- `POST /refresh` - Renovar token
- `GET /me` - Info usuario actual

#### Usuarios (`/api/users`)
- `GET /me` - Mi perfil
- `PUT /me` - Actualizar perfil
- `DELETE /me` - Eliminar cuenta

#### Reservas (`/api/reservations`)
- `POST /` - Crear reserva
- `GET /` - Mis reservas
- `GET /{id}` - Detalle reserva
- `DELETE /{id}` - Cancelar reserva

#### Espacios (`/api/spaces`)
- `GET /` - Listar espacios
- `GET /{id}` - Detalle espacio
- `GET /{id}/availability` - Verificar disponibilidad

**Documentación interactiva**: http://localhost/api/auth/docs (Swagger UI)

---

## 📈 Métricas de Rendimiento

### Resultados de Tests de Carga

| Métrica | Objetivo | Resultado | Status |
|---------|----------|-----------|--------|
| Latencia p95 | <200ms | 189ms | ✅ |
| Throughput | >1000 req/s | 1,850 req/s | ✅ |
| Error Rate | <1% | 0.03% | ✅ |
| Usuarios Concurrentes | >100 | 300 | ✅ |

**Análisis completo**: [Ver Informe de Pruebas](./documentos/04_informe_pruebas.md)

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión | Justificación |
|------------|------------|---------|---------------|
| Backend | FastAPI | 0.109+ | Async, rápido, docs automáticas |
| Lenguaje | Python | 3.11+ | Productividad, ecosistema |
| Base de Datos | PostgreSQL | 15+ | ACID, robustez |
| Caché | Redis | 7+ | Performance |
| Gateway | NGINX | 1.25+ | Estabilidad probada |
| Containers | Docker | 24+ | Estándar industria |
| Testing | pytest + k6 | - | Unitarios + Carga |

**Decisiones detalladas**: [Ver Decisiones Técnicas](./documentos/02_decisiones_tecnicas.md)

---

## 🚦 Guía de Uso Rápida

### 1. Registrar Usuario

```powershell
curl -X POST http://localhost/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"Test123!\",\"name\":\"Usuario Prueba\"}'
```

### 2. Login

```powershell
curl -X POST http://localhost/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"password\":\"Test123!\"}'
```

### 3. Crear Reserva

```powershell
# Guardar token del paso anterior
$token = "tu_token_aqui"

curl -X POST http://localhost/api/reservations `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $token" `
  -d '{\"space_id\":1,\"start_time\":\"2026-02-01T10:00:00\",\"end_time\":\"2026-02-01T12:00:00\"}'
```

---

## 🐛 Troubleshooting

### Problema: Puerto 80 ocupado

```powershell
# Editar docker-compose.yml
# Cambiar: "80:80" por "8080:80"
# Acceder a: http://localhost:8080
```

### Problema: Containers se reinician

```powershell
# Ver logs
docker-compose logs auth-service

# Verificar DB
docker-compose ps postgres
```

**Guía completa**: [Ver Troubleshooting](./documentos/03_guia_despliegue.md#troubleshooting)

---

## 📚 Recursos Adicionales

### Referencias Técnicas
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Patrones y Arquitectura
- [Microservices Patterns](https://microservices.io/patterns/)
- [12 Factor App](https://12factor.net/)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)

---

## 🎯 Objetivos de Aprendizaje Cumplidos

- ✅ Arquitectura de microservicios real y funcional
- ✅ Containerización con Docker y orquestación
- ✅ API RESTful con documentación automática
- ✅ Base de datos relacional con triggers y constraints
- ✅ Testing completo (unitario + integración + carga)
- ✅ Seguridad (JWT, bcrypt, validaciones)
- ✅ Documentación profesional nivel empresa
- ✅ DevOps básico (Docker Compose, health checks)

---

## 👤 Autor

**Daniel Araya**

- 🐙 GitHub: [@D-Araya](https://github.com/D-Araya)
- 📂 Repositorio: [fundamentos_arquitectura_cloud](https://github.com/D-Araya/fundamentos_arquitectura_cloud)
- 📧 Email: [tu-email@ejemplo.com]

---

<div align="center">

**[⬆ Volver arriba](#sistema-de-reservas-en-la-nube---arquitectura-de-microservicios)**

---

**Estado**: ✅ Proyecto Completado y Funcional  
**Testing**: ✅ 87/87 Tests Implementados (100%)  
**Cobertura**: ✅ 90% Promedio  
**Rendimiento**: ✅ p95 < 200ms  
**Documentación**: ✅ Profesional y Completa

---

Made with ❤️ using FastAPI, Docker, PostgreSQL

*Enero 2026*

</div>
