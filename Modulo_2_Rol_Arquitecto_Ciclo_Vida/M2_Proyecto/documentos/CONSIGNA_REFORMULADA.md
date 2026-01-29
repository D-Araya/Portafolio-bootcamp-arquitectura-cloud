# Sistema de Reservas en la Nube - Proyecto de Arquitectura Cloud

## 📋 Descripción del Proyecto

Este proyecto consiste en el diseño e implementación de un **sistema de reservas escalable** basado en arquitectura de microservicios y desplegado en la nube. El sistema permitirá a los usuarios gestionar reservas de espacios y recursos de manera eficiente, con capacidad de adaptación a diferentes cargas de trabajo.

---

## 🎯 Objetivos del Proyecto

### Objetivo General
Diseñar y construir una arquitectura cloud para un sistema de reservas que sea:
- **Escalable**: Capaz de crecer horizontalmente según la demanda
- **Seguro**: Protegiendo la información de usuarios mediante autenticación y encriptación
- **Eficiente**: Manteniendo tiempos de respuesta óptimos bajo diferentes cargas

### Objetivos Específicos
1. Implementar una arquitectura de microservicios desacoplada
2. Garantizar escalabilidad automática ante picos de demanda
3. Asegurar la privacidad y protección de datos de usuarios
4. Facilitar el mantenimiento y evolución del sistema

---

## 📝 Requerimientos

### Requerimientos Funcionales

| ID | Requerimiento | Descripción |
|----|---------------|-------------|
| RF-01 | Crear Reservas | Permitir a usuarios crear nuevas reservas de espacios en tiempo real |
| RF-02 | Consultar Reservas | Visualizar reservas existentes con filtros y búsqueda |
| RF-03 | Cancelar Reservas | Posibilidad de cancelar reservas activas |
| RF-04 | Autenticación | Sistema de login seguro para usuarios |

### Requerimientos No Funcionales

| ID | Categoría | Descripción | Métrica Objetivo |
|----|-----------|-------------|------------------|
| RNF-01 | Escalabilidad | Auto-scaling horizontal de servicios | Soportar 10x carga base |
| RNF-02 | Rendimiento | Tiempo de respuesta óptimo | < 200ms en el percentil 95 |
| RNF-03 | Seguridad | Encriptación de datos sensibles | TLS 1.3, JWT tokens |
| RNF-04 | Disponibilidad | Alta disponibilidad del sistema | 99.9% uptime |
| RNF-05 | Mantenibilidad | Código limpio y bien documentado | Cobertura de tests > 80% |

### Requerimientos Técnicos

- **Arquitectura**: Microservicios con contenedores Docker
- **Documentación**: Diagrama de arquitectura y de clases
- **Testing**: Pruebas unitarias y de rendimiento/carga
- **Código**: Buenas prácticas, legibilidad, y estructura clara

---

## 🔍 Criterios de Evaluación

### 1. Aspectos Técnicos (40 puntos)

#### Escalabilidad y Rendimiento
- La arquitectura debe soportar escalamiento horizontal
- Tiempo de respuesta < 200ms bajo carga normal
- Capacidad de manejar picos de demanda sin degradación

#### Código y Organización
- Código bien estructurado siguiendo principios SOLID
- Nomenclatura clara y consistente
- Separación de responsabilidades
- Uso apropiado de patrones de diseño

#### Documentación Técnica
- Diagrama de arquitectura completo
- Diagrama de clases detallado
- Instrucciones de instalación y despliegue
- Documentación de APIs y servicios

### 2. Aspectos Estructurales (30 puntos)

#### Cumplimiento de Requerimientos
- Todas las funcionalidades implementadas
- Especificaciones técnicas cumplidas
- Arquitectura de microservicios correctamente aplicada

#### Seguridad
- Autenticación implementada (JWT o similar)
- Encriptación de datos sensibles
- Validación de inputs
- Manejo seguro de credenciales

### 3. Aspectos de Performance (30 puntos)

#### Rendimiento bajo Carga
- Pruebas de carga documentadas
- Sistema estable con múltiples usuarios concurrent es
- Métricas de rendimiento registradas

#### Calidad del Diseño
- Patrones de diseño aplicados correctamente
- Bajo acoplamiento entre servicios
- Alta cohesión dentro de cada servicio
- Preparado para evolución futura

---

## 📦 Entregables

### 1. Código Fuente
- Repositorio GitHub con estructura clara
- Todos los microservicios implementados
- Scripts de configuración y despliegue
- Dockerfiles y docker-compose.yml

### 2. Documentación

#### README Principal
- Descripción del proyecto
- Arquitectura general
- Instrucciones de instalación
- Guía de uso
- Enlaces a documentación detallada

#### Documentación Técnica
- Descripción de cada microservicio
- Decisiones arquitectónicas y justificación
- Tecnologías utilizadas y por qué
- Guía de despliegue paso a paso

#### Diagramas
- Diagrama de arquitectura del sistema
- Diagrama de clases
- Diagramas de secuencia (opcional pero recomendado)
- Diagrama de base de datos

### 3. Testing

#### Informe de Pruebas
- Resultados de pruebas unitarias
- Resultados de pruebas de carga
- Análisis de rendimiento
- Problemas identificados y soluciones

#### Código de Pruebas
- Tests unitarios con buena cobertura
- Tests de integración
- Scripts de pruebas de carga

### 4. Presentación
- Resumen ejecutivo del proyecto
- Aspectos técnicos destacados
- Desafíos enfrentados y soluciones
- Demostración del sistema funcionando

---

## 🛠️ Tecnologías Recomendadas

### Backend
- **Lenguaje**: Python (Flask/FastAPI) o Node.js (Express)
- **Base de Datos**: PostgreSQL o MongoDB
- **Caché**: Redis
- **Message Queue**: RabbitMQ o Apache Kafka (opcional)

### Infraestructura
- **Contenedores**: Docker
- **Orquestación**: Docker Compose (local) o Kubernetes (avanzado)
- **Gateway**: NGINX o Kong

### Testing
- **Unitarias**: pytest (Python) o Jest (Node.js)
- **Carga**: JMeter, Locust, o k6
- **Integración**: Postman/Newman

### Monitoring (Opcional)
- **Logs**: ELK Stack o similar
- **Métricas**: Prometheus + Grafana

---

## 📚 Referencias y Recursos

### Documentación Oficial
- [Docker Documentation](https://docs.docker.com/)
- [Microservices Patterns](https://microservices.io/patterns/index.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### Testing
- [pytest Documentation](https://docs.pytest.org/)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [k6 Load Testing](https://k6.io/docs/)

### Buenas Prácticas
- [12 Factor App](https://12factor.net/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [REST API Best Practices](https://restfulapi.net/)

---

## 📊 Estructura del Repositorio

```
fundamentos_arquitectura_cloud/
└── Modulo_2_Arquitectura_Software/
    └── M2_AE4_Pilares_Fundamentales/
        ├── README.md                 # Documentación principal
        ├── codigo/                   # Código fuente
        │   ├── README.md
        │   ├── docker-compose.yml
        │   ├── gateway/
        │   ├── auth-service/
        │   ├── reservations-service/
        │   └── users-service/
        ├── documentos/               # Documentación técnica
        │   ├── 01_arquitectura.md
        │   ├── 02_decisiones_tecnicas.md
        │   ├── 03_guia_despliegue.md
        │   └── 04_informe_pruebas.md
        └── imagenes/                 # Diagramas
            ├── arquitectura_sistema.png
            ├── diagrama_clases.png
            └── diagrama_secuencia.png
```

---

## ✅ Lista de Verificación Final

Antes de entregar, verificar que:

- [ ] Todos los microservicios están implementados y funcionando
- [ ] Docker Compose levanta todos los servicios correctamente
- [ ] Pruebas unitarias pasan exitosamente
- [ ] Pruebas de carga ejecutadas y documentadas
- [ ] README principal completo y claro
- [ ] Documentación técnica detallada
- [ ] Diagramas incluidos en el repositorio
- [ ] Código comentado apropiadamente
- [ ] Informe de pruebas completo
- [ ] Repositorio organizado según estructura definida

---

## 📄 Licencia

Este proyecto es parte del portafolio académico de Arquitectura Cloud.

---

*Última actualización: Enero 2026*