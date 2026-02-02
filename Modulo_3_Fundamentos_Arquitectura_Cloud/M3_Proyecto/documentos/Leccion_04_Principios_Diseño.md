# Lección 4: Principios de Diseño Arquitectónico

## 🏗️ Arquitectura Modular, Resiliente y Escalable

### 🎯 Objetivo de la Lección

Aplicar principios fundamentales de diseño arquitectónico para construir una arquitectura modular, resiliente y segura, consolidando las decisiones tomadas en las lecciones anteriores en un diseño estructurado.

---

## 📋 Tabla de Contenidos

- [1. Principios de Diseño Arquitectónico](#1-principios-de-diseño-arquitectónico)
- [2. Modularidad y Separación de Responsabilidades](#2-modularidad-y-separación-de-responsabilidades)
- [3. Desacoplamiento](#3-desacoplamiento)
- [4. Elasticidad y Escalabilidad](#4-elasticidad-y-escalabilidad)
- [5. Resiliencia y Tolerancia a Fallos](#5-resiliencia-y-tolerancia-a-fallos)
- [6. Esquema Conceptual de la Arquitectura](#6-esquema-conceptual-de-la-arquitectura)
- [7. Documentación de Decisiones](#7-documentación-de-decisiones)
- [8. Conclusiones](#8-conclusiones)

---

## 1. Principios de Diseño Arquitectónico

### 1.1 Framework de Principios

Los principios de diseño arquitectónico son lineamientos fundamentales que guían la construcción de sistemas robustos, mantenibles y escalables.

```
┌────────────────────────────────────────────────┐
│     PRINCIPIOS DE DISEÑO ARQUITECTÓNICO        │
├────────────────────────────────────────────────┤
│                                                │
│  1. 🧩 MODULARIDAD                            │
│     └─ Separación de responsabilidades        │
│                                                │
│  2. 🔗 DESACOPLAMIENTO                        │
│     └─ Independencia entre componentes        │
│                                                │
│  3. ⚡ ELASTICIDAD                            │
│     └─ Escalado dinámico                      │
│                                                │
│  4. 🛡️ RESILIENCIA                           │
│     └─ Tolerancia a fallos                    │
│                                                │
│  5. 🔐 SEGURIDAD POR DISEÑO                   │
│     └─ Protección en múltiples capas          │
│                                                │
└────────────────────────────────────────────────┘
```

### 1.2 Beneficios de Aplicar Principios

| Principio | Beneficio Clave | Impacto en el Proyecto |
|-----------|-----------------|------------------------|
| **Modularidad** | Mantenibilidad | Cambios localizados, sin efecto dominó |
| **Desacoplamiento** | Flexibilidad | Reemplazo de componentes sin afectar sistema |
| **Elasticidad** | Eficiencia | Costos optimizados, recursos bajo demanda |
| **Resiliencia** | Disponibilidad | Sistema operativo ante fallos |
| **Seguridad** | Protección | Defensa en profundidad |

---

## 2. Modularidad y Separación de Responsabilidades

### 2.1 Concepto de Modularidad

**Modularidad** significa dividir el sistema en componentes independientes, cada uno con una responsabilidad específica y bien definida.

> "Un módulo debe hacer una cosa y hacerla bien" - Principio de Responsabilidad Única (SRP)

### 2.2 Evolución: Monolito → Microservicios

#### Arquitectura Monolítica (Antes)

```
┌──────────────────────────────────────────┐
│         APLICACIÓN MONOLÍTICA            │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐ │
│  │    Capa de Presentación            │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │    Lógica de Negocio               │ │
│  │  • Autenticación                   │ │
│  │  • Gestión de Usuarios             │ │
│  │  • Procesamiento de Pedidos        │ │
│  │  • Pagos                           │ │
│  │  • Notificaciones                  │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │    Capa de Datos                   │ │
│  └────────────────────────────────────┘ │
│                                          │
│         Base de Datos Única              │
└──────────────────────────────────────────┘
```

**Problemas del Monolito:**
- ❌ Escalado de toda la aplicación (aunque solo un módulo necesite más recursos)
- ❌ Deploy de todo el sistema por cambio pequeño
- ❌ Fallo en un módulo afecta toda la aplicación
- ❌ Difícil de mantener y evolucionar
- ❌ Acoplamiento alto entre componentes

#### Arquitectura de Microservicios (Ahora)

```
┌─────────────────────────────────────────────────────────┐
│           ARQUITECTURA DE MICROSERVICIOS                │
└─────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Auth       │  │   Users      │  │   Orders     │
│  Service     │  │  Service     │  │  Service     │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ • Login      │  │ • CRUD Users │  │ • Create     │
│ • JWT        │  │ • Profile    │  │ • Track      │
│ • Refresh    │  │ • Preferences│  │ • Update     │
└──────────────┘  └──────────────┘  └──────────────┘
       │                 │                  │
       ▼                 ▼                  ▼
   [DB Auth]        [DB Users]        [DB Orders]

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Payment     │  │ Notification │  │  Analytics   │
│  Service     │  │   Service    │  │   Service    │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ • Process    │  │ • Email      │  │ • Reports    │
│ • Refund     │  │ • SMS        │  │ • Metrics    │
│ • Validate   │  │ • Push       │  │ • Insights   │
└──────────────┘  └──────────────┘  └──────────────┘
       │                 │                  │
       ▼                 ▼                  ▼
  [DB Payment]      [Queue]          [Data Lake]
```

**Beneficios de Microservicios:**
- ✅ Escalado independiente por servicio
- ✅ Deploy independiente (CI/CD por servicio)
- ✅ Fallo aislado (no afecta otros servicios)
- ✅ Equipos independientes por servicio
- ✅ Tecnologías diferentes por servicio si es necesario

### 2.3 Aplicación en Nuestro Proyecto

#### Módulos Identificados

```
PROYECTO NUBE SÓLIDA - MÓDULOS
═══════════════════════════════════════════

┌─────────────────────────────────────────┐
│  MÓDULO 1: API Gateway                  │
│  Responsabilidad: Punto de entrada      │
│  Tecnología: AWS API Gateway (PaaS)     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 2: Authentication Service       │
│  Responsabilidad: Autenticación         │
│  Tecnología: ECS Fargate (PaaS)         │
│  Lenguaje: Node.js                      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 3: User Management Service      │
│  Responsabilidad: Gestión de usuarios   │
│  Tecnología: ECS Fargate (PaaS)         │
│  Lenguaje: Python (FastAPI)             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 4: Business Logic Service       │
│  Responsabilidad: Lógica de negocio     │
│  Tecnología: ECS Fargate (PaaS)         │
│  Lenguaje: Python (FastAPI)             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 5: File Processing              │
│  Responsabilidad: Procesamiento archivos│
│  Tecnología: Lambda (FaaS)              │
│  Lenguaje: Python                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 6: Notification Service         │
│  Responsabilidad: Envío notificaciones  │
│  Tecnología: Lambda + SQS (FaaS)        │
│  Lenguaje: Python                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 7: Data Layer                   │
│  Responsabilidad: Persistencia          │
│  Tecnología: RDS PostgreSQL (PaaS)      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  MÓDULO 8: Storage                      │
│  Responsabilidad: Archivos estáticos    │
│  Tecnología: S3 (IaaS)                  │
└─────────────────────────────────────────┘
```

#### Tabla de Responsabilidades

| Módulo | Responsabilidad Única | Expone API | Consume API |
|--------|----------------------|------------|-------------|
| **API Gateway** | Enrutamiento, rate limiting | ✅ REST | ECS Services |
| **Auth Service** | Login, JWT, sesiones | ✅ REST | User Service |
| **User Service** | CRUD usuarios | ✅ REST | RDS |
| **Business Service** | Lógica core negocio | ✅ REST | RDS, S3 |
| **File Processing** | Transform archivos | ❌ Event | S3 |
| **Notification** | Enviar emails/SMS | ❌ Queue | SES/SNS |
| **Data Layer** | Persistencia | ❌ DB | - |
| **Storage** | Archivos estáticos | ❌ Object Storage | - |

### 2.4 Ventajas de Nuestra Modularidad

1. **Mantenimiento Simplificado**
   - Cada equipo puede trabajar en su módulo
   - Bug en Auth Service no requiere tocar Business Service
   - Testing aislado por módulo

2. **Escalabilidad Independiente**
   ```
   Scenario: Black Friday
   ├─ Business Service: Escala 10x (alto tráfico)
   ├─ Auth Service: Escala 2x (logins)
   └─ User Service: No escala (poco uso)
   
   Resultado: Costo optimizado, recursos donde se necesitan
   ```

3. **Deploy Independiente**
   ```
   git push feature/new-payment-method
   └─ Deploy solo Payment Service
      ├─ Otros servicios no afectados
      ├─ Rollback solo Payment si hay problemas
      └─ Zero downtime deployment
   ```

---

## 3. Desacoplamiento

### 3.1 Concepto de Desacoplamiento

**Desacoplamiento** significa minimizar las dependencias directas entre componentes, permitiendo que evolucionen independientemente.

> "Los componentes deben comunicarse a través de interfaces bien definidas, no mediante implementaciones concretas"

### 3.2 Niveles de Acoplamiento

```
ACOPLAMIENTO FUERTE (❌ Evitar)
═══════════════════════════════
Service A ──[direct call]──> Service B
           ←──[response]────

Problema:
• Si B falla, A falla
• Deploy de B requiere coordinar con A
• Cambios en B impactan A
```

```
ACOPLAMIENTO DÉBIL (✅ Implementar)
═════════════════════════════════
Service A ──[message]──> Queue ──> Service B

Beneficios:
• Si B falla, mensaje queda en queue
• A y B se despliegan independientemente
• Cambios en B no impactan A (contrato estable)
```

### 3.3 Estrategias de Desacoplamiento

#### 3.3.1 Comunicación Asíncrona con Colas

**Problema sin Queue:**
```python
# Service A llama directamente a Service B
def process_order(order_id):
    # Si Service B está caído, esto falla
    result = requests.post('http://service-b/notify', json={'order_id': order_id})
    if result.status_code != 200:
        # ¿Qué hacemos? ¿Reintentar? ¿Perder la notificación?
        raise Exception("Notification failed")
```

**Solución con SQS (Queue):**
```python
import boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/123456/notifications-queue'

def process_order(order_id):
    # Enviamos mensaje a queue y continuamos
    # Si Service B está caído, el mensaje espera en queue
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({
            'order_id': order_id,
            'type': 'order_completed',
            'timestamp': datetime.now().isoformat()
        })
    )
    # Continuamos sin esperar respuesta
    return {'status': 'processing'}
```

**Service B (Consumer):**
```python
# Service B procesa cuando esté disponible
def notification_worker():
    while True:
        messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        
        for message in messages.get('Messages', []):
            try:
                body = json.loads(message['Body'])
                send_email(body['order_id'])
                
                # Eliminar mensaje de queue solo si se procesó correctamente
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Mensaje volverá a queue para reintento
```

**Ventajas:**
- ✅ Service A no se bloquea esperando a B
- ✅ Si B está caído, mensajes se acumulan en queue
- ✅ Reintento automático de mensajes fallidos
- ✅ Escalado independiente de consumers

#### 3.3.2 Event-Driven con EventBridge

**Arquitectura Event-Driven:**
```
┌─────────────────────────────────────────────────┐
│            EVENT-DRIVEN ARCHITECTURE            │
└─────────────────────────────────────────────────┘

┌──────────────┐
│ Order Service│
└──────┬───────┘
       │ Publica evento:
       │ "order.created"
       ▼
┌──────────────────┐
│   EventBridge    │  (Event Bus)
└─────┬──────┬─────┘
      │      │
      ▼      ▼
┌──────────┐ ┌─────────────┐ ┌──────────────┐
│Inventory │ │  Shipping   │ │ Notification │
│ Service  │ │  Service    │ │   Service    │
└──────────┘ └─────────────┘ └──────────────┘

Todos reaccionan al mismo evento,
pero no se conocen entre sí
```

**Ejemplo Práctico:**
```python
# Order Service publica evento
import boto3

eventbridge = boto3.client('events')

def create_order(order_data):
    # Crear orden en DB
    order = db.save_order(order_data)
    
    # Publicar evento
    eventbridge.put_events(
        Entries=[{
            'Source': 'orders.service',
            'DetailType': 'OrderCreated',
            'Detail': json.dumps({
                'order_id': order.id,
                'customer_id': order.customer_id,
                'total': order.total,
                'items': order.items
            }),
            'EventBusName': 'default'
        }]
    )
    
    return order
```

```python
# Inventory Service escucha evento (Lambda)
def lambda_handler(event, context):
    detail = event['detail']
    order_id = detail['order_id']
    items = detail['items']
    
    # Reducir inventario
    for item in items:
        reduce_stock(item['product_id'], item['quantity'])
    
    logger.info(f"Inventory updated for order {order_id}")
```

```python
# Shipping Service escucha el MISMO evento (Lambda)
def lambda_handler(event, context):
    detail = event['detail']
    
    # Crear envío
    shipment = create_shipment(
        order_id=detail['order_id'],
        customer_id=detail['customer_id']
    )
    
    logger.info(f"Shipment created: {shipment.id}")
```

**Ventajas:**
- ✅ Order Service no conoce Inventory ni Shipping
- ✅ Agregar nuevo subscriber no requiere cambios en publisher
- ✅ Evolución independiente de servicios

#### 3.3.3 API Gateway como Abstracción

**API Gateway oculta implementación interna:**
```
CLIENTE VE:
https://api.nubesolida.com/v1/users

API GATEWAY ENRUTA A:
http://user-service-internal:8080/users

BENEFICIOS:
• Cliente no conoce dónde está el servicio
• Podemos cambiar implementación sin afectar cliente
• Podemos balancear carga entre múltiples instancias
```

### 3.4 Contratos y Versionado de APIs

**Evitar Breaking Changes:**
```json
// API v1 (actual)
{
  "id": 123,
  "name": "John Doe"
}

// API v2 (nueva versión - NO BREAKING)
{
  "id": 123,
  "name": "John Doe",
  "full_name": "John Alexander Doe",  // Nuevo campo
  "email": "john@example.com"          // Nuevo campo
}

// Clientes v1 siguen funcionando (ignoran campos nuevos)
```

**Versionado en API Gateway:**
```
/v1/users  →  User Service v1
/v2/users  →  User Service v2

Estrategia de migración:
1. Mantener v1 funcionando
2. Lanzar v2 en paralelo
3. Migrar clientes gradualmente
4. Deprecar v1 después de 6 meses
```

---

## 4. Elasticidad y Escalabilidad

### 4.1 Concepto de Elasticidad

**Elasticidad** es la capacidad de un sistema de ajustar automáticamente sus recursos en función de la demanda.

```
ELASTICIDAD EN ACCIÓN
═══════════════════════════════════════

Lunes 9 AM (Bajo tráfico)
Instancias: 2
Costo: $50/día
        ┌───┐ ┌───┐
        │ 1 │ │ 2 │
        └───┘ └───┘

Viernes 8 PM (Alto tráfico)
Instancias: 8
Costo: $200/día
┌───┐ ┌───┐ ┌───┐ ┌───┐
│ 1 │ │ 2 │ │ 3 │ │ 4 │
└───┘ └───┘ └───┘ └───┘
┌───┐ ┌───┐ ┌───┐ ┌───┐
│ 5 │ │ 6 │ │ 7 │ │ 8 │
└───┘ └───┘ └───┘ └───┘

Sábado 3 AM (Muy bajo tráfico)
Instancias: 1
Costo: $25/día
        ┌───┐
        │ 1 │
        └───┘
```

### 4.2 Tipos de Escalado

#### 4.2.1 Escalado Vertical (Scale Up)

```
ANTES:                  DESPUÉS:
┌────────────┐         ┌────────────┐
│  t3.small  │   →     │ t3.xlarge  │
│  2 vCPU    │         │  4 vCPU    │
│  2 GB RAM  │         │ 16 GB RAM  │
└────────────┘         └────────────┘
```

**Características:**
- ✅ Simple (cambiar tipo de instancia)
- ❌ Requiere downtime (reinicio)
- ❌ Límite físico (no infinito)
- ⚠️ SPOF (Single Point of Failure)

**Cuándo usar:**
- Bases de datos (RDS)
- Aplicaciones legacy monolíticas
- Cargas de trabajo que no se pueden distribuir

#### 4.2.2 Escalado Horizontal (Scale Out)

```
ANTES:                  DESPUÉS:
┌────────────┐         ┌────────────┐ ┌────────────┐
│ Instancia 1│   →     │ Instancia 1│ │ Instancia 2│
└────────────┘         └────────────┘ └────────────┘
                       ┌────────────┐ ┌────────────┐
                       │ Instancia 3│ │ Instancia 4│
                       └────────────┘ └────────────┘
```

**Características:**
- ✅ Sin downtime (agregar instancias)
- ✅ Infinitamente escalable
- ✅ Alta disponibilidad (múltiples instancias)
- ⚠️ Requiere stateless apps

**Cuándo usar:**
- APIs stateless
- Microservicios
- Aplicaciones web modernas

### 4.3 Implementación en Nuestro Proyecto

#### 4.3.1 Auto Scaling para ECS Fargate

**Configuración de Auto Scaling:**
```yaml
# AWS ECS Task Definition con Auto Scaling
---
AutoScalingConfiguration:
  ServiceName: api-service
  
  MinCapacity: 2          # Mínimo para HA
  MaxCapacity: 10         # Máximo por costos
  DesiredCapacity: 2      # Inicial
  
  ScalingPolicies:
    - PolicyName: ScaleUp
      MetricType: CPUUtilization
      TargetValue: 70      # % de CPU
      ScaleOutCooldown: 60  # segundos
      ScaleInCooldown: 300  # segundos
      
    - PolicyName: ScaleByRequests
      MetricType: RequestCountPerTarget
      TargetValue: 1000    # requests por instancia
      
  HealthCheck:
    Path: /health
    Interval: 30
    Timeout: 5
    HealthyThreshold: 2
    UnhealthyThreshold: 3
```

**Ejemplo de Auto Scaling en Acción:**
```
TIMELINE DE AUTO SCALING
════════════════════════════════════════════

10:00 AM
├─ Tráfico: 500 req/min
├─ CPU: 40%
└─ Instancias: 2 (sin cambios)

10:30 AM (Pico de tráfico)
├─ Tráfico: 3000 req/min
├─ CPU: 85%
├─ Trigger: CPU > 70%
└─ Acción: Agregar 2 instancias
   └─ Instancias: 4

10:35 AM
├─ Nuevas instancias activas
├─ CPU: 55% (distribuido)
└─ Sistema estable

12:00 PM (Pico máximo)
├─ Tráfico: 8000 req/min
├─ CPU: 80%
└─ Acción: Agregar 4 instancias
   └─ Instancias: 8

3:00 PM (Tráfico baja)
├─ Tráfico: 1500 req/min
├─ CPU: 35%
├─ Trigger: CPU < 40% por 5 min
└─ Acción: Remover 3 instancias
   └─ Instancias: 5

11:00 PM (Madrugada)
├─ Tráfico: 300 req/min
├─ CPU: 25%
└─ Acción: Escalar a mínimo
   └─ Instancias: 2
```

#### 4.3.2 Lambda: Escalado Infinito Automático

**Lambda escala automáticamente:**
```
Concurrencia Lambda (sin configuración manual)
═════════════════════════════════════════════

Request 1    →  [Lambda 1]
Request 2    →  [Lambda 2]
Request 3    →  [Lambda 3]
...
Request 1000 →  [Lambda 1000]

AWS gestiona automáticamente:
• Provisión de recursos
• Distribución de carga
• Sin configuración de Auto Scaling
• Límite: 1000 ejecuciones concurrentes (aumentable)
```

#### 4.3.3 RDS: Read Replicas para Escalado de Lectura

**Patrón Master-Replica:**
```
┌───────────────────────────────────────────┐
│         RDS SCALING STRATEGY              │
└───────────────────────────────────────────┘

APPLICATION
      │
      ├─ WRITES (10%)
      │     ↓
      │  ┌──────────────┐
      │  │ RDS Primary  │
      │  │  (Master)    │
      │  └──────────────┘
      │        │
      │        │ Replication
      │        ├───────────────┐
      │        ▼               ▼
      │  ┌──────────┐    ┌──────────┐
      │  │ Replica 1│    │ Replica 2│
      │  └──────────┘    └──────────┘
      │        ▲               ▲
      └─ READS (90%) ─────────┘
```

**Configuración:**
```python
# Configuración de conexiones DB
DB_CONFIG = {
    'write': {
        'host': 'nube-solida.cluster-xxxx.us-east-1.rds.amazonaws.com',
        'port': 5432
    },
    'read': [
        'nube-solida.cluster-ro-xxxx.us-east-1.rds.amazonaws.com'
    ]
}

# Uso en aplicación
def get_user(user_id):
    # Lectura → usar read replica
    conn = connect_db(DB_CONFIG['read'][0])
    return conn.query("SELECT * FROM users WHERE id = %s", user_id)

def update_user(user_id, data):
    # Escritura → usar primary
    conn = connect_db(DB_CONFIG['write'])
    return conn.execute("UPDATE users SET ... WHERE id = %s", user_id)
```

### 4.4 Métricas de Escalabilidad

| Métrica | Valor Objetivo | Acción de Escalado |
|---------|----------------|-------------------|
| **CPU Utilization** | 70% | Scale out si > 80% por 2 min |
| **Memory Utilization** | 75% | Scale out si > 85% por 2 min |
| **Request Count** | 1000 req/target | Scale out si > 1200 |
| **Response Time p99** | < 500ms | Scale out si > 800ms |
| **Error Rate** | < 1% | Alerta + investigar |

---

## 5. Resiliencia y Tolerancia a Fallos

### 5.1 Concepto de Resiliencia

**Resiliencia** es la capacidad de un sistema de continuar operando (posiblemente con funcionalidad degradada) cuando ocurren fallos.

> "No es SI un componente fallará, sino CUÁNDO fallará" - Principio de Diseño Resiliente

### 5.2 Estrategias de Resiliencia

#### 5.2.1 Multi-AZ (Availability Zones)

**Arquitectura Multi-AZ:**
```
┌────────────────────────────────────────────────────┐
│              AWS REGION: us-east-1                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │   AZ-1a             │  │   AZ-1b             │ │
│  ├─────────────────────┤  ├─────────────────────┤ │
│  │                     │  │                     │ │
│  │  ┌──────────────┐   │  │  ┌──────────────┐  │ │
│  │  │ ECS Task 1   │   │  │  │ ECS Task 2   │  │ │
│  │  └──────────────┘   │  │  └──────────────┘  │ │
│  │                     │  │                     │ │
│  │  ┌──────────────┐   │  │  ┌──────────────┐  │ │
│  │  │ RDS Primary  │───┼──┼─>│ RDS Standby  │  │ │
│  │  └──────────────┘   │  │  └──────────────┘  │ │
│  │                     │  │                     │ │
│  └─────────────────────┘  └─────────────────────┘ │
│                                                    │
│  Si AZ-1a falla completamente (datacenter down):  │
│  • ECS Task 2 (AZ-1b) continúa sirviendo         │
│  • RDS Standby se promueve a Primary (1-2 min)   │
│  • ALB redirige todo el tráfico a AZ-1b          │
└────────────────────────────────────────────────────┘
```

**Configuración Multi-AZ en Terraform:**
```hcl
resource "aws_ecs_service" "api" {
  name            = "api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 4
  
  # Distribuir en múltiples AZ
  network_configuration {
    subnets = [
      aws_subnet.private_1a.id,  # AZ-1a
      aws_subnet.private_1b.id   # AZ-1b
    ]
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
}
```

#### 5.2.2 Health Checks y Auto-Recovery

**Health Checks en ALB:**
```yaml
HealthCheck:
  Protocol: HTTP
  Path: /health
  Port: 8080
  
  Interval: 30           # Check cada 30 segundos
  Timeout: 5             # Timeout de 5 segundos
  
  HealthyThreshold: 2    # 2 checks OK = healthy
  UnhealthyThreshold: 3  # 3 checks FAIL = unhealthy
  
  SuccessCodes: "200"    # HTTP 200 = healthy
```

**Implementación de /health endpoint:**
```python
from fastapi import FastAPI, Response
import psycopg2

app = FastAPI()

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Verifica que la app y sus dependencias estén funcionando
    """
    checks = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check 1: Aplicación corriendo
    checks['checks']['app'] = 'ok'
    
    # Check 2: Conexión a base de datos
    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        conn.cursor().execute('SELECT 1')
        conn.close()
        checks['checks']['database'] = 'ok'
    except Exception as e:
        checks['status'] = 'unhealthy'
        checks['checks']['database'] = f'error: {str(e)}'
    
    # Check 3: Memoria disponible
    import psutil
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 90:
        checks['status'] = 'degraded'
        checks['checks']['memory'] = f'warning: {memory_percent}%'
    else:
        checks['checks']['memory'] = 'ok'
    
    status_code = 200 if checks['status'] == 'healthy' else 503
    return Response(content=json.dumps(checks), status_code=status_code)
```

**Comportamiento de Auto-Recovery:**
```
TIMELINE DE AUTO-RECOVERY
════════════════════════════════════════

10:00:00 - Instancia A funcionando normal
         └─ Health check: OK (200)

10:05:00 - Instancia A comienza a fallar
         ├─ Health check 1: FAIL (503)
         ├─ Health check 2: FAIL (timeout)
         └─ Health check 3: FAIL (timeout)
         
10:05:30 - ALB marca Instancia A como "unhealthy"
         └─ Tráfico redirigido a Instancia B

10:05:35 - ECS detecta instancia unhealthy
         ├─ Termina Instancia A
         └─ Lanza Instancia A' (nueva)

10:07:00 - Instancia A' inicia
         ├─ Health check 1: OK
         └─ Health check 2: OK

10:07:30 - ALB marca Instancia A' como "healthy"
         └─ Instancia A' recibe tráfico nuevamente
```

#### 5.2.3 Circuit Breaker Pattern

**Problema sin Circuit Breaker:**
```
Service A llama a Service B (que está caído)
└─ Espera timeout (30 seg)
   └─ Reintenta
      └─ Espera timeout (30 seg)
         └─ Reintenta
            └─ Usuario espera 90 segundos para error
```

**Solución con Circuit Breaker:**
```python
from circuitbreaker import circuit

# Configuración del circuit breaker
@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_service(data):
    """
    Si falla 5 veces, el circuit se "abre"
    Durante 60 segundos, las llamadas fallan inmediatamente
    Después, intenta una llamada de prueba
    """
    response = requests.post('http://external-service/api', json=data)
    response.raise_for_status()
    return response.json()

# Uso con fallback
def process_payment(payment_data):
    try:
        result = call_external_service(payment_data)
        return result
    except CircuitBreakerError:
        # Circuit abierto - servicio caído
        # Fallback: guardar para procesar después
        logger.warning("Payment service down, queuing payment")
        queue_payment(payment_data)
        return {'status': 'queued', 'message': 'Payment will be processed later'}
```

**Estados del Circuit Breaker:**
```
┌─────────────────────────────────────────┐
│     CIRCUIT BREAKER STATES              │
└─────────────────────────────────────────┘

CLOSED (Normal)
├─ Llamadas pasan normalmente
├─ Si failures < threshold: mantener CLOSED
└─ Si failures >= threshold: → OPEN

OPEN (Servicio caído)
├─ Llamadas fallan inmediatamente
├─ No se intenta llamar al servicio
├─ Después de timeout: → HALF-OPEN
└─ Usuarios reciben respuesta rápida

HALF-OPEN (Probando recuperación)
├─ Permite UNA llamada de prueba
├─ Si éxito: → CLOSED
└─ Si falla: → OPEN
```

#### 5.2.4 Retry con Exponential Backoff

**Estrategia de Reintentos:**
```python
import time
import random

def exponential_backoff_retry(func, max_retries=5):
    """
    Reintenta con espera exponencial
    Retry 1: 1 segundo
    Retry 2: 2 segundos
    Retry 3: 4 segundos
    Retry 4: 8 segundos
    Retry 5: 16 segundos
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                # Último intento falló
                raise
            
            # Calcular espera con jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s")
            time.sleep(wait_time)

# Uso
result = exponential_backoff_retry(lambda: call_api())
```

#### 5.2.5 Graceful Degradation

**Degradación Elegante:**
```python
def get_user_recommendations(user_id):
    """
    Intenta obtener recomendaciones personalizadas
    Si falla, devuelve recomendaciones genéricas
    """
    try:
        # Servicio de ML para recomendaciones personalizadas
        recommendations = ml_service.get_personalized_recommendations(user_id)
        return recommendations
    except Exception as e:
        logger.error(f"ML service failed: {e}")
        
        # Fallback: recomendaciones populares (cache)
        return cache.get('popular_items')[:10]
```

### 5.3 Backup y Disaster Recovery

#### 5.3.1 Estrategia de Backups

**RDS Automated Backups:**
```yaml
RDS Backup Configuration:
  AutomatedBackups:
    Enabled: true
    RetentionPeriod: 7 days
    BackupWindow: "03:00-04:00 UTC"
    
  Snapshots:
    Manual: Created before deployments
    Retention: 30 days
    
  Point-in-Time Recovery:
    Enabled: true
    Window: Last 7 days (cualquier momento)
```

**S3 Versioning y Lifecycle:**
```hcl
resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  
  rule {
    id     = "archive-old-versions"
    status = "Enabled"
    
    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }
    
    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}
```

#### 5.3.2 RTO y RPO

**Objetivos de Recuperación:**
```
┌──────────────────────────────────────────────┐
│  DISASTER RECOVERY OBJECTIVES                │
├──────────────────────────────────────────────┤
│                                              │
│  RTO (Recovery Time Objective)               │
│  └─ Tiempo máximo de downtime aceptable     │
│     Nuestro objetivo: < 15 minutos           │
│                                              │
│  RPO (Recovery Point Objective)              │
│  └─ Pérdida máxima de datos aceptable       │
│     Nuestro objetivo: < 5 minutos            │
│                                              │
└──────────────────────────────────────────────┘

TIMELINE DE DESASTRE:
════════════════════════════════════════════════

10:00 AM - Sistema funcionando normal
         └─ Último backup: 9:55 AM (5 min atrás)

10:05 AM - DESASTRE: AZ-1a falla completamente
         ├─ RDS Primary caído
         └─ 2 de 4 ECS tasks caídos

10:06 AM - Failover automático inicia
         ├─ RDS Standby (AZ-1b) → Primary
         └─ ECS lanza tasks en AZ-1b

10:07 AM - Sistema recuperado
         ├─ RTO logrado: 2 minutos ✅
         ├─ RPO logrado: 5 minutos ✅
         └─ Pérdida de datos: Transacciones entre 10:05-10:06

RESULTADO:
• Downtime: 2 minutos (objetivo: <15 min) ✅
• Datos perdidos: ~1 minuto de transacciones
• Sistema operativo con funcionalidad completa
```

---

## 6. Esquema Conceptual de la Arquitectura

### 6.1 Diagrama de Arquitectura Completo

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     ARQUITECTURA "NUBE SÓLIDA"                             │
│                      CLIENTE-SERVIDOR MULTI-AZ                             │
│                         (AWS - us-east-1)                                  │
└────────────────────────────────────────────────────────────────────────────┘

                              INTERNET
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌─────────┐  ┌─────────┐  ┌─────────┐
              │ Cliente │  │ Cliente │  │ Cliente │
              │   Web   │  │  Móvil  │  │   API   │
              └─────────┘  └─────────┘  └─────────┘
                    │            │            │
                    └────────────┼────────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │   Route 53    │
                         │  (DNS Global) │
                         └───────────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │  CloudFront   │
                         │  (CDN + WAF)  │
                         └───────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────────────┐
│                            VPC (10.0.0.0/16)                                │
├────────────────────────────────┼────────────────────────────────────────────┤
│                                ▼                                            │
│                        ┌───────────────┐                                    │
│                        │ API Gateway   │                                    │
│                        │(Rate Limiting)│                                    │
│                        └───────────────┘                                    │
│                                │                                            │
│  ┌─────────────────────────────┼─────────────────────────────┐             │
│  │          PUBLIC SUBNET (Multi-AZ)                          │             │
│  ├────────────────────────────────────────────────────────────┤             │
│  │                            ▼                               │             │
│  │                  ┌──────────────────────┐                  │             │
│  │                  │ Application Load     │                  │             │
│  │                  │ Balancer (ALB)       │                  │             │
│  │                  │ • Health Checks      │                  │             │
│  │                  │ • SSL Termination    │                  │             │
│  │                  └──────────────────────┘                  │             │
│  │                            │                               │             │
│  │     ┌──────────────────────┼──────────────────────┐        │             │
│  │     │                      │                      │        │             │
│  │  ┌──▼────┐              ┌──▼────┐              ┌──▼────┐  │             │
│  │  │  NAT  │              │  NAT  │              │  NAT  │  │             │
│  │  │Gateway│              │Gateway│              │Gateway│  │             │
│  │  │ AZ-A  │              │ AZ-B  │              │ AZ-C  │  │             │
│  │  └───────┘              └───────┘              └───────┘  │             │
│  └─────────────────────────────────────────────────────────┘             │
│                                │                                            │
│  ┌─────────────────────────────┼─────────────────────────────┐             │
│  │          PRIVATE SUBNET (Multi-AZ)                         │             │
│  ├────────────────────────────────────────────────────────────┤             │
│  │                            ▼                               │             │
│  │                                                            │             │
│  │  ┌──────────────────────────────────────────────────────┐ │             │
│  │  │              ECS FARGATE CLUSTER                     │ │             │
│  │  ├──────────────────────────────────────────────────────┤ │             │
│  │  │                                                      │ │             │
│  │  │  AZ-A                       AZ-B                     │ │             │
│  │  │  ┌─────────────────┐       ┌─────────────────┐     │ │             │
│  │  │  │  Auth Service   │       │  Auth Service   │     │ │             │
│  │  │  │  (Task 1)       │       │  (Task 2)       │     │ │             │
│  │  │  └─────────────────┘       └─────────────────┘     │ │             │
│  │  │                                                      │ │             │
│  │  │  ┌─────────────────┐       ┌─────────────────┐     │ │             │
│  │  │  │  User Service   │       │  User Service   │     │ │             │
│  │  │  │  (Task 1)       │       │  (Task 2)       │     │ │             │
│  │  │  └─────────────────┘       └─────────────────┘     │ │             │
│  │  │                                                      │ │             │
│  │  │  ┌─────────────────┐       ┌─────────────────┐     │ │             │
│  │  │  │Business Service │       │Business Service │     │ │             │
│  │  │  │  (Task 1)       │       │  (Task 2)       │     │ │             │
│  │  │  └─────────────────┘       └─────────────────┘     │ │             │
│  │  │                                                      │ │             │
│  │  └──────────────────────────────────────────────────────┘ │             │
│  │                            │                               │             │
│  │         ┌──────────────────┼──────────────────┐           │             │
│  │         │                  │                  │           │             │
│  │         ▼                  ▼                  ▼           │             │
│  │  ┌────────────┐     ┌────────────┐     ┌────────────┐   │             │
│  │  │  Lambda    │     │    SQS     │     │EventBridge │   │             │
│  │  │ Functions  │     │  (Queue)   │     │   (Bus)    │   │             │
│  │  │            │     │            │     │            │   │             │
│  │  │• File Proc │     │• Notif     │     │• Events    │   │             │
│  │  │• Thumbnail │     │• Emails    │     │• Webhooks  │   │             │
│  │  └────────────┘     └────────────┘     └────────────┘   │             │
│  │         │                  │                  │           │             │
│  │         └──────────────────┼──────────────────┘           │             │
│  │                            │                               │             │
│  │         ┌──────────────────┼──────────────────┐           │             │
│  │         ▼                  ▼                  ▼           │             │
│  │  ┌────────────┐     ┌────────────┐     ┌────────────┐   │             │
│  │  │    RDS     │     │     S3     │     │CloudWatch  │   │             │
│  │  │PostgreSQL  │     │  Storage   │     │   Logs     │   │             │
│  │  │            │     │            │     │            │   │             │
│  │  │• Primary   │     │• Files     │     │• Metrics   │   │             │
│  │  │  (AZ-A)    │     │• Backups   │     │• Alerts    │   │             │
│  │  │• Standby   │     │• Static    │     │• Dashboard │   │             │
│  │  │  (AZ-B)    │     │            │     │            │   │             │
│  │  └────────────┘     └────────────┘     └────────────┘   │             │
│  │                                                            │             │
│  └────────────────────────────────────────────────────────────┘             │
│                                                                              │
│  SECURITY LAYERS:                                                           │
│  ├─ VPC Isolation                                                          │
│  ├─ Security Groups (Stateful Firewall)                                    │
│  ├─ Network ACLs (Stateless Firewall)                                      │
│  ├─ IAM Roles & Policies (Least Privilege)                                 │
│  ├─ AWS WAF (Application Firewall)                                         │
│  ├─ Secrets Manager (Credentials)                                          │
│  └─ KMS (Encryption Keys)                                                  │
└──────────────────────────────────────────────────────────────────────────────┘

SERVICIOS DE OBSERVABILIDAD:
├─ CloudWatch: Logs, Metrics, Dashboards, Alarms
├─ CloudTrail: API Audit Logs
├─ X-Ray: Distributed Tracing
└─ GuardDuty: Threat Detection
```

### 6.2 Modelo Cliente-Servidor Detallado

**Representación Visual:**

![Modelo Cliente-Servidor](../imagenes/diagrama_cliente_servidor.png)


**Representación ASCII (texto):**

```
┌────────────────────────────────────────────────────────────┐
│              MODELO CLIENTE-SERVIDOR                       │
└────────────────────────────────────────────────────────────┘

CAPA DE CLIENTE
═══════════════════════════════════════════════════════════

┌─────────────────┐
│   WEB CLIENT    │
├─────────────────┤
│ • React SPA     │
│ • Hosted in S3  │
│ • CloudFront    │
│ • REST API      │
└─────────────────┘

┌─────────────────┐
│  MOBILE CLIENT  │
├─────────────────┤
│ • React Native  │
│ • iOS + Android │
│ • REST API      │
│ • Push Notif    │
└─────────────────┘

┌─────────────────┐
│   API CLIENT    │
├─────────────────┤
│ • External Apps │
│ • Integrations  │
│ • Webhooks      │
└─────────────────┘

         │
         │ HTTPS / TLS 1.3
         │ JSON / REST
         ▼

CAPA DE SERVIDOR
═══════════════════════════════════════════════════════════

┌─────────────────────────────────────────┐
│     API GATEWAY (Entry Point)           │
├─────────────────────────────────────────┤
│ • Authentication (JWT)                  │
│ • Rate Limiting                         │
│ • Request Validation                    │
│ • Routing                               │
└─────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│     LOAD BALANCER (ALB)                 │
├─────────────────────────────────────────┤
│ • Health Checks                         │
│ • SSL Termination                       │
│ • Path-based Routing                    │
│ • Sticky Sessions                       │
└─────────────────────────────────────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
         ▼         ▼         ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│   Auth     │ │   User     │ │  Business  │
│  Service   │ │  Service   │ │  Service   │
├────────────┤ ├────────────┤ ├────────────┤
│• Login     │ │• CRUD      │ │• Core      │
│• JWT       │ │• Profile   │ │• Logic     │
│• Sessions  │ │• Prefs     │ │• Rules     │
└────────────┘ └────────────┘ └────────────┘
         │         │         │
         └─────────┼─────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│     DATA & STORAGE LAYER                │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐   ┌────────────────┐ │
│  │ RDS Primary  │   │  S3 Storage    │ │
│  │ PostgreSQL   │   │  (Files)       │ │
│  └──────────────┘   └────────────────┘ │
│         │                               │
│         ▼                               │
│  ┌──────────────┐                       │
│  │ RDS Standby  │                       │
│  │ (Replica)    │                       │
│  └──────────────┘                       │
│                                         │
└─────────────────────────────────────────┘

PROCESAMIENTO ASÍNCRONO
═══════════════════════════════════════════════════════════

┌──────────────┐    ┌───────────┐    ┌──────────────┐
│    SQS       │───>│  Lambda   │───>│ Notification │
│   Queue      │    │ Consumer  │    │   Service    │
└──────────────┘    └───────────┘    └──────────────┘

┌──────────────┐    ┌───────────┐    ┌──────────────┐
│ EventBridge  │───>│  Lambda   │───>│ Analytics    │
│    Bus       │    │ Processor │    │   Service    │
└──────────────┘    └───────────┘    └──────────────┘
```

### 6.3 Flujo de Datos: Request Usuario → Respuesta

```
FLUJO COMPLETO DE UNA PETICIÓN
═══════════════════════════════════════════════════════════

1. USUARIO hace request
   ↓
   GET https://app.nubesolida.com/api/v1/users/123
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

2. DNS (Route 53)
   ↓
   Resuelve: app.nubesolida.com → CloudFront

3. CDN (CloudFront)
   ↓
   • Verifica cache (MISS)
   • Forward a Origin (ALB)

4. WAF valida
   ↓
   • No malicious patterns
   • Rate limit OK
   • ALLOW request

5. API Gateway
   ↓
   • Valida JWT
   • Extrae user_id del token
   • Route: /users/:id → user-service

6. Application Load Balancer
   ↓
   • Health check targets
   • Select healthy instance (AZ-A)
   • Forward to ECS Task

7. ECS Fargate (User Service)
   ↓
   async def get_user(user_id: int):
       # Consulta DB
       user = await db.query(
           "SELECT * FROM users WHERE id = $1",
           user_id
       )
       return user

8. RDS PostgreSQL (Read Replica)
   ↓
   • Query: SELECT * FROM users WHERE id = 123
   • Return: {"id": 123, "name": "John", ...}

9. User Service responde
   ↓
   {
     "id": 123,
     "name": "John Doe",
     "email": "john@example.com",
     "created_at": "2024-01-01T00:00:00Z"
   }

10. ALB → API Gateway → CloudFront → Usuario
    ↓
    Status: 200 OK
    Time: 145ms

11. CloudWatch registra
    ↓
    • Latency: 145ms
    • Status: 200
    • User: 123
    • Timestamp: ...

═══════════════════════════════════════════════════════════
TOTAL TIME: 145ms
• DNS: 5ms
• CloudFront: 20ms
• WAF: 10ms
• API Gateway: 15ms
• ALB: 10ms
• User Service: 50ms
• Database: 30ms
• Response: 5ms
═══════════════════════════════════════════════════════════
```

---

## 7. Documentación de Decisiones

### 7.1 Architecture Decision Records (ADR)

#### ADR-001: Adopción de Microservicios

**Estado:** Aprobado  
**Fecha:** 2026-01-15  
**Decisores:** Equipo de Arquitectura

**Contexto:**
Necesitamos decidir entre arquitectura monolítica o microservicios para el nuevo sistema cloud.

**Decisión:**
Adoptamos arquitectura de microservicios con los siguientes servicios:
- Auth Service
- User Service
- Business Service
- Notification Service (async)
- File Processing Service (serverless)

**Justificación:**
1. Escalabilidad independiente por servicio
2. Deploy independiente (menos riesgo)
3. Equipos independientes (mayor velocidad)
4. Fallo aislado (mejor resiliencia)
5. Flexibilidad tecnológica

**Consecuencias:**
- ✅ Mejor escalabilidad y resiliencia
- ✅ Mayor velocidad de desarrollo
- ⚠️ Mayor complejidad operacional
- ⚠️ Requiere observabilidad avanzada
- ⚠️ Testing de integración más complejo

**Alternativas Consideradas:**
- Monolito modular: Descartado por escalabilidad limitada
- Serverless completo: Descartado por cold starts y límites

---

#### ADR-002: Multi-AZ Deployment

**Estado:** Aprobado  
**Fecha:** 2026-01-16

**Contexto:**
Necesitamos definir estrategia de alta disponibilidad.

**Decisión:**
Desplegar en múltiples Availability Zones (AZ-A, AZ-B) con:
- ECS tasks distribuidos en ambas AZ
- RDS Multi-AZ con failover automático
- ALB distribuyendo tráfico entre AZ

**Justificación:**
1. RTO < 15 minutos (objetivo cumplido)
2. Resiliencia ante fallo de datacenter completo
3. Costo moderado (~30% más vs single-AZ)
4. Simplicidad vs multi-region

**Consecuencias:**
- ✅ Alta disponibilidad 99.9%+
- ✅ Failover automático < 2 min
- ✅ Sin complejidad de multi-region
- ⚠️ Costo adicional ~$150/mes

---

#### ADR-003: Comunicación Asíncrona con SQS

**Estado:** Aprobado  
**Fecha:** 2026-01-17

**Contexto:**
Decidir patrón de comunicación entre microservicios.

**Decisión:**
- Síncrono (REST): Para operaciones críticas (Auth, Read)
- Asíncrono (SQS): Para operaciones no-críticas (Notifications, File Processing)

**Justificación:**
1. Desacoplamiento de servicios
2. Resiliencia (mensajes persisten en queue)
3. Throttling natural (consumers procesan a su ritmo)
4. Retry automático de mensajes fallidos

**Consecuencias:**
- ✅ Mejor resiliencia
- ✅ Escalado independiente de producers/consumers
- ⚠️ Eventual consistency (no inmediato)
- ⚠️ Complejidad de debugging

---

### 7.2 Tabla Resumen de Decisiones Arquitectónicas

| ID | Decisión | Razón Principal | Trade-off |
|----|----------|-----------------|-----------|
| **ADR-001** | Microservicios | Escalabilidad independiente | Mayor complejidad |
| **ADR-002** | Multi-AZ | Alta disponibilidad | Costo +30% |
| **ADR-003** | Async con SQS | Desacoplamiento | Eventual consistency |
| **ADR-004** | ECS Fargate | Sin gestión servidores | Costo vs EC2 |
| **ADR-005** | RDS vs NoSQL | Relaciones y ACID | Escalabilidad horizontal limitada |
| **ADR-006** | Lambda para eventos | Costo optimizado | Cold starts |
| **ADR-007** | S3 para archivos | Durabilidad 99.999999999% | Latencia vs EBS |
| **ADR-008** | ALB vs NLB | HTTP/HTTPS + path routing | Performance vs simplicidad |

---

## 8. Conclusiones

### 8.1 Logros de la Lección 4

✅ **Principios Aplicados:**
- Modularidad: Sistema dividido en 8 módulos independientes
- Desacoplamiento: Comunicación via APIs, queues y eventos
- Elasticidad: Auto-scaling automático en todos los componentes
- Resiliencia: Multi-AZ, health checks, circuit breakers
- Seguridad: Diseñada en múltiples capas

✅ **Diseño Conceptual Completo:**
- Arquitectura cliente-servidor bien definida
- Flujos de datos documentados
- Componentes con responsabilidades claras
- Decisiones arquitectónicas justificadas

✅ **Consolidación de Decisiones:**
- Modelos de servicio (Lección 2) integrados
- Modelo de implementación (Lección 3) aplicado
- Principios de diseño implementados

### 8.2 Próximos Pasos

En la **Lección 5** completaremos la arquitectura incorporando:

1. **Atributos de Calidad Detallados:**
   - Seguridad: WAF, IAM, Encryption, Secrets Management
   - Escalabilidad: Políticas de auto-scaling detalladas
   - Resiliencia: Disaster recovery, backups, monitoring

2. **Estrategias Específicas:**
   - Configuraciones de seguridad
   - Métricas y alarmas
   - Procedimientos operacionales

3. **Documentación Final:**
   - Integración de todos los componentes
   - Validación de cumplimiento de requisitos
   - Plan de implementación

---

## 📚 Referencias

### Principios de Diseño
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Microservices Patterns - Chris Richardson](https://microservices.io/patterns/index.html)
- [Release It! - Michael Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/)

### Resiliencia
- [Circuit Breaker Pattern - Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html)
- [AWS Multi-AZ Deployments](https://aws.amazon.com/rds/features/multi-az/)

### Monitoreo
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/)

---

[← Volver: Lección 3](./Leccion_03_Modelos_Implementacion.md) | [Siguiente: Lección 5 →](./Leccion_05_Atributos_Calidad.md)
