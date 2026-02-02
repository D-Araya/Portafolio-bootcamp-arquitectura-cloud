# Lección 2: Modelos de Servicio en la Nube

## ☁️ IaaS, PaaS, SaaS y FaaS

### 🎯 Objetivo de la Lección

Seleccionar y justificar los modelos de servicio (IaaS, PaaS, SaaS, FaaS) adecuados para cada componente de la arquitectura cliente-servidor.

---

## 📋 Tabla de Contenidos

- [1. Introducción a los Modelos de Servicio](#1-introducción-a-los-modelos-de-servicio)
- [2. Infrastructure as a Service (IaaS)](#2-infrastructure-as-a-service-iaas)
- [3. Platform as a Service (PaaS)](#3-platform-as-a-service-paas)
- [4. Software as a Service (SaaS)](#4-software-as-a-service-saas)
- [5. Function as a Service (FaaS)](#5-function-as-a-service-faas)
- [6. Comparativa de Modelos](#6-comparativa-de-modelos)
- [7. Arquitectura Cliente-Servidor del Proyecto](#7-arquitectura-cliente-servidor-del-proyecto)
- [8. Asignación de Modelos a Componentes](#8-asignación-de-modelos-a-componentes)
- [9. Conclusiones](#9-conclusiones)

---

## 1. Introducción a los Modelos de Servicio

### La Pirámide de Servicios Cloud

```
        ┌───────────────┐
        │     SaaS      │  Software completo (Gmail, Salesforce)
        ├───────────────┤
        │     PaaS      │  Plataforma de desarrollo (Heroku, App Engine)
        ├───────────────┤
        │     IaaS      │  Infraestructura virtualizada (EC2, VMs)
        └───────────────┘
               │
        ┌───────────────┐
        │     FaaS      │  Funciones sin servidor (Lambda, Azure Functions)
        └───────────────┘
```

### Concepto Fundamental

Los **modelos de servicio** definen el **nivel de abstracción** y **responsabilidad compartida** entre el proveedor cloud y el cliente.

### Modelo de Responsabilidad Compartida

| Componente | On-Premise | IaaS | PaaS | SaaS |
|------------|------------|------|------|------|
| **Aplicaciones** | 👤 Cliente | 👤 Cliente | 👤 Cliente | ☁️ Proveedor |
| **Datos** | 👤 Cliente | 👤 Cliente | 👤 Cliente | ☁️ Proveedor |
| **Runtime** | 👤 Cliente | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor |
| **Middleware** | 👤 Cliente | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor |
| **SO** | 👤 Cliente | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor |
| **Virtualización** | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor | ☁️ Proveedor |
| **Servidores** | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor | ☁️ Proveedor |
| **Almacenamiento** | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor | ☁️ Proveedor |
| **Networking** | 👤 Cliente | ☁️ Proveedor | ☁️ Proveedor | ☁️ Proveedor |

**Leyenda:**
- 👤 = Gestionado por el cliente
- ☁️ = Gestionado por el proveedor cloud

---

## 2. Infrastructure as a Service (IaaS)

### 2.1 Definición

**IaaS** proporciona recursos de infraestructura virtualizados bajo demanda: servidores, almacenamiento, redes y sistemas operativos.

> "Alquila el hardware, pero controlas todo el software"

### 2.2 Características Principales

#### Control Máximo
- Acceso root/administrador al SO
- Configuración completa del sistema
- Instalación de cualquier software

#### Responsabilidades del Cliente
```
Cliente gestiona:
  ├── Sistema Operativo
  ├── Parches y actualizaciones de SO
  ├── Aplicaciones
  ├── Middleware
  ├── Runtime
  └── Datos

Proveedor gestiona:
  ├── Hardware físico
  ├── Virtualización
  ├── Almacenamiento físico
  └── Red física
```

### 2.3 Servicios IaaS Principales

#### Amazon Web Services (AWS)

| Servicio | Descripción | Caso de Uso |
|----------|-------------|-------------|
| **EC2** | Máquinas virtuales escalables | Servidores de aplicaciones |
| **EBS** | Block storage persistente | Discos de VMs |
| **S3** | Object storage | Archivos, backups, data lakes |
| **VPC** | Red privada virtual | Aislamiento de red |
| **ELB** | Balanceador de carga | Distribución de tráfico |

#### Microsoft Azure

| Servicio | Descripción |
|----------|-------------|
| **Virtual Machines** | VMs Windows/Linux |
| **Blob Storage** | Object storage |
| **Virtual Network** | Redes privadas |
| **Load Balancer** | Distribución de tráfico |

#### Google Cloud Platform

| Servicio | Descripción |
|----------|-------------|
| **Compute Engine** | VMs |
| **Persistent Disk** | Block storage |
| **Cloud Storage** | Object storage |
| **VPC** | Redes privadas |

### 2.4 Ventajas de IaaS

| Ventaja | Descripción |
|---------|-------------|
| 🎛️ **Control Total** | Configuración completa del stack |
| 🚀 **Escalabilidad** | Ajuste dinámico de recursos |
| 💰 **Costo-Efectivo** | Pago por uso, sin CAPEX |
| 🌍 **Disponibilidad Global** | Deploy en múltiples regiones |
| 🔧 **Flexibilidad** | Cualquier SO o software |

### 2.5 Desventajas de IaaS

| Desventaja | Descripción |
|------------|-------------|
| 🔧 **Mantenimiento** | Cliente gestiona OS, parches, seguridad |
| 👥 **Skills requeridos** | Necesita conocimientos de sysadmin |
| ⏰ **Time-to-Market** | Mayor tiempo de configuración inicial |

### 2.6 Casos de Uso Ideales

- ✅ **Migración Lift-and-Shift** de aplicaciones existentes
- ✅ **Control granular** sobre configuración del sistema
- ✅ **Aplicaciones legacy** que requieren SO específico
- ✅ **Alto rendimiento** con configuraciones custom
- ✅ **Entornos de desarrollo** y testing flexibles

### 2.7 Ejemplo Práctico: Servidor Web con IaaS

```bash
# Crear instancia EC2 (AWS CLI ejemplo)
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.medium \
    --key-name mi-key-pair \
    --security-group-ids sg-0123456789abcdef0 \
    --subnet-id subnet-0123456789abcdef0 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=WebServer}]'

# Conectarse a la instancia
ssh -i mi-key-pair.pem ec2-user@ec2-xx-xxx-xxx-xx.compute.amazonaws.com

# Instalar servidor web
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd

# Configurar aplicación
cd /var/www/html
sudo vi index.html
```

**Responsabilidad del cliente:**
- Configurar SO
- Instalar y configurar Apache
- Gestionar seguridad y parches
- Monitorear y mantener

---

## 3. Platform as a Service (PaaS)

### 3.1 Definición

**PaaS** proporciona una plataforma completa de desarrollo y despliegue, abstrayendo la infraestructura subyacente.

> "Enfócate en tu código, no en la infraestructura"

### 3.2 Características Principales

#### Abstracción de Infraestructura
- No gestionas SO ni servidores
- Escalado automático
- Alta disponibilidad integrada

#### Responsabilidades del Cliente
```
Cliente gestiona:
  ├── Aplicaciones
  ├── Datos
  └── Configuración de la aplicación

Proveedor gestiona:
  ├── Sistema Operativo
  ├── Runtime (Java, Python, Node.js, etc.)
  ├── Middleware
  ├── Virtualización
  └── Hardware
```

### 3.3 Servicios PaaS Principales

#### AWS

| Servicio | Descripción | Lenguajes Soportados |
|----------|-------------|----------------------|
| **Elastic Beanstalk** | PaaS managed | Java, .NET, PHP, Node.js, Python, Ruby, Go |
| **RDS** | Base de datos gestionada | MySQL, PostgreSQL, Oracle, SQL Server |
| **ECS/EKS** | Contenedores gestionados | Docker, Kubernetes |

#### Azure

| Servicio | Descripción |
|----------|-------------|
| **App Service** | Web apps y APIs |
| **Azure SQL Database** | SQL Server gestionado |
| **Azure Functions** | Serverless functions |
| **Azure Kubernetes Service** | Kubernetes gestionado |

#### Google Cloud

| Servicio | Descripción |
|----------|-------------|
| **App Engine** | PaaS fully managed |
| **Cloud Run** | Contenedores serverless |
| **Cloud SQL** | Bases de datos gestionadas |
| **GKE** | Kubernetes gestionado |

### 3.4 Ventajas de PaaS

| Ventaja | Descripción |
|---------|-------------|
| ⚡ **Velocidad de Desarrollo** | Deploy en minutos |
| 🔧 **Sin gestión de infraestructura** | Foco en código |
| 📈 **Escalado automático** | Sin intervención manual |
| 🔒 **Seguridad integrada** | Parches automáticos |
| 💰 **Costo optimizado** | Pago por uso real |

### 3.5 Desventajas de PaaS

| Desventaja | Descripción |
|------------|-------------|
| 🔒 **Menos control** | Configuraciones limitadas |
| 🔗 **Vendor lock-in** | Dependencia del proveedor |
| 🎨 **Menos flexibilidad** | Limitado a runtimes soportados |

### 3.6 Casos de Uso Ideales

- ✅ **Aplicaciones web modernas** (microservicios, APIs)
- ✅ **Startups** que necesitan velocidad
- ✅ **Desarrollo ágil** con CI/CD
- ✅ **Equipos pequeños** sin DevOps dedicado
- ✅ **MVPs** y prototipos rápidos

### 3.7 Ejemplo Práctico: API REST con PaaS

```yaml
# Ejemplo con AWS Elastic Beanstalk
# archivo: .ebextensions/app.config

option_settings:
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.micro
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 10
  aws:elasticbeanstalk:environment:
    EnvironmentType: LoadBalanced

# Deploy con un comando
eb deploy
```

```python
# app.py - Código de aplicación
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Responsabilidad del cliente:**
- Solo escribir código
- Configurar variables de entorno
- Deploy con un comando

**Proveedor gestiona:**
- Servidores
- Load balancer
- Auto-scaling
- Monitoreo
- Parches de SO

---

## 4. Software as a Service (SaaS)

### 4.1 Definición

**SaaS** proporciona aplicaciones completas listas para usar, accesibles vía web browser o APIs.

> "Usa el software, no lo construyas ni lo mantengas"

### 4.2 Características Principales

#### Aplicación Lista para Usar
- Sin instalación local
- Acceso vía navegador web
- Actualizaciones automáticas
- Multi-tenant

#### Responsabilidades del Cliente
```
Cliente gestiona:
  └── Datos y configuración de usuario

Proveedor gestiona:
  ├── Aplicación
  ├── Datos de la aplicación
  ├── Runtime
  ├── Middleware
  ├── SO
  └── Infraestructura completa
```

### 4.3 Ejemplos de SaaS

#### Productividad
- **Google Workspace** (Gmail, Docs, Drive)
- **Microsoft 365** (Outlook, Word, Excel, Teams)
- **Slack** (Comunicación empresarial)
- **Zoom** (Videoconferencias)

#### CRM y Ventas
- **Salesforce** (CRM líder)
- **HubSpot** (Marketing y ventas)
- **Zendesk** (Soporte al cliente)

#### Gestión de Proyectos
- **Jira** (Gestión ágil)
- **Asana** (Gestión de tareas)
- **Trello** (Tableros Kanban)
- **Monday.com** (Work OS)

#### Desarrollo y DevOps
- **GitHub** (Control de versiones)
- **GitLab** (DevOps platform)
- **Datadog** (Monitoreo)

### 4.4 Ventajas de SaaS

| Ventaja | Descripción |
|---------|-------------|
| 🚀 **Time-to-Value inmediato** | Usar desde día 1 |
| 💰 **Costo predecible** | Suscripción mensual/anual |
| 🔧 **Zero mantenimiento** | Actualizaciones automáticas |
| 🌐 **Acceso universal** | Desde cualquier dispositivo |
| 👥 **Colaboración** | Multi-usuario en tiempo real |

### 4.5 Desventajas de SaaS

| Desventaja | Descripción |
|------------|-------------|
| 🎨 **Poca personalización** | Funcionalidad estándar |
| 🔗 **Vendor lock-in** | Dependencia total del proveedor |
| 🔒 **Control de datos** | Datos en servidores del proveedor |
| 🌐 **Requiere internet** | No disponible offline (generalmente) |

### 4.6 Casos de Uso Ideales

- ✅ **Herramientas de productividad** (email, documentos)
- ✅ **CRM y ERP** empresariales
- ✅ **Comunicación y colaboración** de equipos
- ✅ **Aplicaciones estándar** sin personalización
- ✅ **Necesidades de negocio** no core

---

## 5. Function as a Service (FaaS)

### 5.1 Definición

**FaaS** (también llamado **Serverless**) permite ejecutar código en respuesta a eventos, sin gestionar servidores.

> "Ejecuta solo cuando lo necesitas, paga solo por ejecución"

### 5.2 Características Principales

#### Event-Driven
- Ejecución basada en eventos
- Escalado automático a cero
- Pago por milisegundos de ejecución

#### Sin Gestión de Servidores
```
Developer escribe:
  └── Función (código)

Proveedor gestiona:
  ├── Provisión de recursos
  ├── Escalado
  ├── Alta disponibilidad
  ├── Runtime
  └── Infraestructura completa
```

### 5.3 Servicios FaaS Principales

#### AWS Lambda

| Característica | Detalle |
|----------------|---------|
| **Lenguajes** | Python, Node.js, Java, Go, C#, Ruby |
| **Memoria** | 128 MB - 10 GB |
| **Timeout** | Hasta 15 minutos |
| **Pricing** | $0.20 por 1M requests + $0.0000166667 por GB-segundo |

#### Azure Functions

| Característica | Detalle |
|----------------|---------|
| **Lenguajes** | C#, JavaScript, F#, Java, Python, PowerShell |
| **Triggers** | HTTP, Timer, Queue, Blob, Event Grid, etc. |
| **Plans** | Consumption, Premium, Dedicated |

#### Google Cloud Functions

| Característica | Detalle |
|----------------|---------|
| **Lenguajes** | Node.js, Python, Go, Java, .NET, Ruby, PHP |
| **Triggers** | HTTP, Cloud Storage, Pub/Sub, Firestore |
| **Generation** | 1st gen, 2nd gen (Cloud Run-based) |

### 5.4 Arquitectura Event-Driven

```
┌──────────────┐      Event       ┌─────────────┐
│   Trigger    │ ────────────────> │   Lambda    │
│  (API GW,    │                   │  Function   │
│   S3, etc)   │                   └─────────────┘
└──────────────┘                          │
                                          ▼
                                   ┌─────────────┐
                                   │  Recursos   │
                                   │  (DB, S3)   │
                                   └─────────────┘
```

### 5.5 Ventajas de FaaS

| Ventaja | Descripción |
|---------|-------------|
| 💰 **Costo ultra-optimizado** | Pago por ejecución real |
| ⚡ **Escalado infinito** | Automático e instantáneo |
| 🔧 **Zero administración** | Sin servidores que gestionar |
| ⏱️ **Desarrollo rápido** | Foco solo en lógica de negocio |
| 🎯 **Ideal para eventos** | Procesamiento on-demand |

### 5.6 Desventajas de FaaS

| Desventaja | Descripción |
|------------|-------------|
| ⏰ **Cold Start** | Latencia en primera invocación |
| 🔒 **Límites de tiempo** | Timeout máximo (15 min AWS) |
| 🔧 **Debugging complejo** | Más difícil que apps tradicionales |
| 💰 **Costo en high-volume** | Puede ser caro con tráfico constante |

### 5.7 Casos de Uso Ideales

- ✅ **Procesamiento de eventos** (uploads de archivos, mensajes)
- ✅ **APIs ligeras** con tráfico variable
- ✅ **Tareas programadas** (cron jobs)
- ✅ **Procesamiento de imágenes/video** on-demand
- ✅ **Backend para aplicaciones móviles**
- ✅ **Integraciones y webhooks**

### 5.8 Ejemplo Práctico: Procesamiento de Imágenes

```python
# AWS Lambda function
import boto3
from PIL import Image
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Trigger: S3 - cuando se sube una imagen
    Acción: Crear thumbnail
    """
    
    # Obtener información del evento
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Descargar imagen original
    file_byte_string = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
    img = Image.open(io.BytesIO(file_byte_string))
    
    # Crear thumbnail
    img.thumbnail((200, 200))
    
    # Guardar thumbnail
    buffer = io.BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)
    
    # Subir thumbnail a S3
    thumbnail_key = f'thumbnails/{key}'
    s3_client.put_object(Bucket=bucket, Key=thumbnail_key, Body=buffer)
    
    return {
        'statusCode': 200,
        'body': f'Thumbnail created: {thumbnail_key}'
    }
```

**Flujo:**
1. Usuario sube imagen a S3
2. S3 trigger invoca Lambda automáticamente
3. Lambda procesa imagen y crea thumbnail
4. Guarda resultado en S3
5. Lambda se apaga automáticamente

**Costo ejemplo:**
- 1000 imágenes procesadas/día
- 500ms de ejecución por imagen
- 512MB memoria
- Costo mensual: ~$0.50

---

## 6. Comparativa de Modelos

### 6.1 Tabla Comparativa Completa

| Aspecto | IaaS | PaaS | SaaS | FaaS |
|---------|------|------|------|------|
| **Control** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| **Flexibilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Facilidad de uso** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Time-to-Market** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Costo inicial** | Bajo | Bajo | Bajo | Muy Bajo |
| **Escalabilidad** | Manual/Auto | Automática | N/A | Infinita |
| **Mantenimiento** | Alto | Bajo | Nulo | Nulo |
| **Skills requeridos** | Alto | Medio | Bajo | Medio |
| **Vendor lock-in** | Bajo | Medio | Alto | Alto |

### 6.2 Cuándo Usar Cada Modelo

```
┌─────────────────────────────────────────────────────────┐
│  DECISION TREE: ¿Qué modelo elegir?                    │
└─────────────────────────────────────────────────────────┘

¿Necesitas una aplicación completa y estándar?
│
├─ SÍ ──> SaaS (Ej: CRM, Email, Office)
│
└─ NO ──> ¿Necesitas ejecutar código solo cuando ocurra un evento?
           │
           ├─ SÍ ──> FaaS (Ej: Procesamiento de archivos, webhooks)
           │
           └─ NO ──> ¿Quieres enfocarte solo en código de aplicación?
                      │
                      ├─ SÍ ──> PaaS (Ej: Web app, API, microservicios)
                      │
                      └─ NO ──> ¿Necesitas control total del sistema?
                                 │
                                 └─ SÍ ──> IaaS (Ej: App legacy, software específico)
```

### 6.3 Casos de Uso por Modelo

| Modelo | Casos de Uso Óptimos |
|--------|---------------------|
| **IaaS** | • Lift-and-shift de apps existentes<br>• Control granular de configuración<br>• Software legacy<br>• Entornos de desarrollo |
| **PaaS** | • Aplicaciones web modernas<br>• APIs REST/GraphQL<br>• Microservicios<br>• Desarrollo ágil |
| **SaaS** | • Herramientas de productividad<br>• CRM/ERP empresariales<br>• Colaboración de equipos<br>• Herramientas estándar |
| **FaaS** | • Procesamiento event-driven<br>• Backends para móviles<br>• Tareas programadas<br>• Procesamiento de datos on-demand |

---

## 7. Arquitectura Cliente-Servidor del Proyecto

### 7.1 Contexto: Proyecto "Nube Sólida"

Recordemos que diseñamos una arquitectura para:
- Modernizar servicios
- Mejorar disponibilidad
- Resolver problemas de escalabilidad
- Reducir costos
- Aumentar resiliencia

### 7.2 Arquitectura Cliente-Servidor Propuesta

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA CONCEPTUAL                  │
└─────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                     CAPA DE CLIENTE                       │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Web App    │  │  Mobile App  │  │  Desktop App │  │
│  │   (React)    │  │ (React Native│  │   (Electron) │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                 │                   │          │
│         └─────────────────┴───────────────────┘          │
│                           │                              │
│                           ▼                              │
│                  ┌──────────────────┐                    │
│                  │   API Gateway    │                    │
│                  │   (CDN + WAF)    │                    │
│                  └──────────────────┘                    │
└───────────────────────────│───────────────────────────────┘
                            │
                            │ HTTPS
                            │
┌───────────────────────────┼───────────────────────────────┐
│                     CAPA DE SERVIDOR                      │
├───────────────────────────┼───────────────────────────────┤
│                           ▼                               │
│              ┌─────────────────────────┐                  │
│              │   Load Balancer (ELB)   │                  │
│              └─────────────────────────┘                  │
│                     │           │                         │
│         ┌───────────┴───────────┴──────────┐              │
│         ▼                                  ▼              │
│  ┌─────────────┐                   ┌─────────────┐       │
│  │  API Layer  │                   │ Microservicios│      │
│  │  (PaaS/     │                   │  (Containers) │      │
│  │   Beanstalk)│                   │   (ECS/EKS)   │      │
│  └─────────────┘                   └─────────────┘       │
│         │                                  │              │
│         └──────────────┬───────────────────┘              │
│                        │                                  │
│         ┌──────────────┼──────────────┐                   │
│         ▼              ▼              ▼                   │
│  ┌──────────┐  ┌──────────────┐  ┌───────────┐          │
│  │    RDS   │  │  Lambda      │  │ S3 Storage│          │
│  │(Database)│  │ (Functions)  │  │  (Files)  │          │
│  └──────────┘  └──────────────┘  └───────────┘          │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 7.3 Componentes Identificados

| Layer | Componente | Función |
|-------|------------|---------|
| **Cliente** | Web App | Interfaz de usuario web |
| **Cliente** | Mobile App | Aplicación móvil |
| **Cliente** | API Gateway | Punto de entrada + seguridad |
| **Servidor** | Load Balancer | Distribución de tráfico |
| **Servidor** | API Layer | Lógica de negocio principal |
| **Servidor** | Microservicios | Servicios especializados |
| **Servidor** | Lambda Functions | Procesamiento event-driven |
| **Datos** | RDS | Base de datos relacional |
| **Datos** | S3 | Almacenamiento de archivos |

---

## 8. Asignación de Modelos a Componentes

### 8.1 Metodología de Asignación

Para cada componente, evaluaremos:
1. **Requisitos de control** (¿cuánto control necesitamos?)
2. **Complejidad operacional** (¿recursos para gestionar?)
3. **Escalabilidad** (¿patrones de demanda?)
4. **Costo** (¿optimización de recursos?)
5. **Time-to-market** (¿velocidad de desarrollo?)

### 8.2 Asignaciones Detalladas

#### 🌐 Componente 1: Web Application (Cliente)

**Modelo Asignado:** **SaaS** para hosting + **CDN**

**Servicio específico:** 
- **AWS S3 + CloudFront** (hosting estático)
- **Netlify/Vercel** (alternativa PaaS)

**Justificación:**
- ✅ Aplicación React estática, no requiere servidor
- ✅ **S3 + CloudFront** distribuye contenido globalmente
- ✅ **Costo mínimo** (centavos por mes para tráfico bajo)
- ✅ **Alta disponibilidad** con CDN global
- ✅ **Zero mantenimiento** de infraestructura
- ✅ **Escalado automático** sin límites

**Modelo de servicio:** SaaS (CDN as a Service)

```bash
# Deploy de React app en S3
aws s3 sync build/ s3://my-webapp-bucket --acl public-read
aws cloudfront create-invalidation --distribution-id E1234 --paths "/*"
```

---

#### 📱 Componente 2: Mobile Application Backend

**Modelo Asignado:** **PaaS** + **FaaS**

**Servicio específico:**
- **AWS Amplify** (PaaS para mobile)
- **Firebase** (alternativa Google)

**Justificación:**
- ✅ Backend como servicio especializado para móviles
- ✅ **Autenticación** integrada (Cognito/Firebase Auth)
- ✅ **APIs** auto-generadas
- ✅ **Push notifications** incluidas
- ✅ **Offline sync** nativo
- ✅ **Time-to-market** extremadamente rápido

**Modelo de servicio:** PaaS (Backend as a Service)

---

#### 🚪 Componente 3: API Gateway

**Modelo Asignado:** **PaaS**

**Servicio específico:**
- **AWS API Gateway**
- **Azure API Management**
- **Google Cloud Endpoints**

**Justificación:**
- ✅ Servicio completamente gestionado
- ✅ **WAF integrado** (Web Application Firewall)
- ✅ **Rate limiting** automático
- ✅ **Autenticación/Autorización** (JWT, OAuth)
- ✅ **Logging y monitoreo** incluidos
- ✅ **Escalado automático** infinito
- ✅ **Costo por request** (pay-per-use)

**Modelo de servicio:** PaaS

```yaml
# Ejemplo API Gateway config (OpenAPI)
openapi: 3.0.0
paths:
  /users:
    get:
      x-amazon-apigateway-integration:
        uri: arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:123456789012:function:GetUsers/invocations
        httpMethod: POST
        type: aws_proxy
```

---

#### ⚖️ Componente 4: Load Balancer

**Modelo Asignado:** **PaaS**

**Servicio específico:**
- **AWS Elastic Load Balancer (ALB)**
- **Azure Load Balancer**
- **Google Cloud Load Balancing**

**Justificación:**
- ✅ Servicio gestionado sin servidores
- ✅ **Alta disponibilidad** multi-AZ automática
- ✅ **Health checks** integrados
- ✅ **SSL/TLS** gestionado
- ✅ **Path-based routing** para microservicios
- ✅ **Auto-scaling** integrado con target groups

**Modelo de servicio:** PaaS

---

#### 🎯 Componente 5: API Layer (Backend Principal)

**Modelo Asignado:** **PaaS**

**Servicio específico:**
- **AWS Elastic Beanstalk**
- **Azure App Service**
- **Google App Engine**

**Justificación:**
- ✅ **Foco en código**, no en infraestructura
- ✅ Soporta múltiples lenguajes (Node.js, Python, Java)
- ✅ **CI/CD integrado**
- ✅ **Auto-scaling** basado en métricas
- ✅ **Zero-downtime deployments**
- ✅ **Monitoreo y logging** incluidos
- ✅ **Costo optimizado** para tráfico variable

**Alternativa con Contenedores (también PaaS):**
- **AWS ECS Fargate** (serverless containers)
- **Azure Container Instances**
- **Google Cloud Run**

**Modelo de servicio:** PaaS

```python
# app.py - Código de aplicación (ejemplo FastAPI)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.get("/users")
async def get_users():
    return {"users": [...]}

@app.post("/users")
async def create_user(user: User):
    # Lógica de creación
    return {"id": "123", **user.dict()}

# Deploy con un comando
# eb init && eb create production
```

---

#### 🔷 Componente 6: Microservicios Especializados

**Modelo Asignado:** **PaaS** (Contenedores gestionados)

**Servicio específico:**
- **AWS ECS Fargate / EKS**
- **Azure Kubernetes Service (AKS)**
- **Google Kubernetes Engine (GKE)**

**Justificación:**
- ✅ **Microservicios** requieren orquestación
- ✅ **Kubernetes gestionado** sin gestionar masters
- ✅ **Escalado independiente** por servicio
- ✅ **Service discovery** automático
- ✅ **Rolling updates** zero-downtime
- ✅ **Portabilidad** entre clouds (Kubernetes estándar)

**Modelo de servicio:** PaaS (CaaS - Containers as a Service)

```yaml
# Ejemplo Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment
  template:
    metadata:
      labels:
        app: payment
    spec:
      containers:
      - name: payment
        image: myrepo/payment-service:v1.2
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: payment-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: payment
```

---

#### ⚡ Componente 7: Procesamiento Event-Driven

**Modelo Asignado:** **FaaS**

**Servicio específico:**
- **AWS Lambda**
- **Azure Functions**
- **Google Cloud Functions**

**Justificación:**
- ✅ **Event-driven** por naturaleza (uploads, webhooks, crons)
- ✅ **Costo ultra-optimizado** (pago por ejecución)
- ✅ **Escalado automático** a millones de ejecuciones
- ✅ **Zero mantenimiento** de servidores
- ✅ **Time-to-market** rápido

**Casos de uso en nuestro proyecto:**
1. **Procesamiento de imágenes** subidas por usuarios
2. **Generación de reportes** (triggered por horario)
3. **Webhooks** de terceros (pagos, notificaciones)
4. **ETL** de datos (transformación on-demand)

**Modelo de servicio:** FaaS

```python
# lambda_image_processor.py
import boto3
import os
from PIL import Image

s3 = boto3.client('s3')

def handler(event, context):
    """
    Trigger: S3 upload
    Procesamiento: Crear thumbnail y extraer metadatos
    """
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Descargar imagen
    download_path = f'/tmp/{os.path.basename(key)}'
    s3.download_file(bucket, key, download_path)
    
    # Procesar
    with Image.open(download_path) as img:
        # Crear thumbnail
        img.thumbnail((200, 200))
        thumb_path = f'/tmp/thumb_{os.path.basename(key)}'
        img.save(thumb_path)
        
        # Subir thumbnail
        thumb_key = f'thumbnails/{os.path.basename(key)}'
        s3.upload_file(thumb_path, bucket, thumb_key)
    
    return {'statusCode': 200, 'thumbnail': thumb_key}
```

---

#### 🗄️ Componente 8: Base de Datos Relacional

**Modelo Asignado:** **PaaS**

**Servicio específico:**
- **AWS RDS** (Aurora, PostgreSQL, MySQL)
- **Azure SQL Database**
- **Google Cloud SQL**

**Justificación:**
- ✅ **Base de datos gestionada** sin administrar servidores
- ✅ **Backups automáticos** diarios
- ✅ **Alta disponibilidad** multi-AZ
- ✅ **Parches automáticos** de seguridad
- ✅ **Escalado vertical** simple (cambiar instance type)
- ✅ **Read replicas** para escalado horizontal de lectura
- ✅ **Monitoreo integrado** (Performance Insights)

**Alternativa IaaS (No recomendada):**
- EC2 + PostgreSQL self-hosted
- ❌ Requiere gestionar: backups, HA, parches, monitoreo
- ❌ Mayor complejidad operacional

**Modelo de servicio:** PaaS (DBaaS - Database as a Service)

```sql
-- Ejemplo de conexión desde aplicación
-- No hay diferencia en el código SQL vs on-premise
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
SELECT * FROM users WHERE email = 'john@example.com';
```

---

#### 📦 Componente 9: Almacenamiento de Archivos

**Modelo Asignado:** **IaaS** (Object Storage)

**Servicio específico:**
- **AWS S3**
- **Azure Blob Storage**
- **Google Cloud Storage**

**Justificación:**
- ✅ **Object storage** escalable ilimitadamente
- ✅ **Alta durabilidad** (99.999999999% - 11 nines)
- ✅ **Versionado** de archivos
- ✅ **Lifecycle policies** para optimizar costos
- ✅ **CDN integration** (CloudFront)
- ✅ **Costo muy bajo** ($0.023/GB/mes)
- ✅ **APIs simples** (REST/SDK)

**Casos de uso:**
- Archivos subidos por usuarios (imágenes, PDFs)
- Backups de base de datos
- Data lakes para analytics
- Archivos estáticos (web hosting)

**Modelo de servicio:** IaaS (aunque el servicio es muy abstracto)

```python
# Ejemplo de uso de S3 desde Python
import boto3

s3 = boto3.client('s3')

# Subir archivo
s3.upload_file('local_file.jpg', 'my-bucket', 'uploads/file.jpg')

# Descargar archivo
s3.download_file('my-bucket', 'uploads/file.jpg', 'downloaded_file.jpg')

# Listar archivos
response = s3.list_objects_v2(Bucket='my-bucket', Prefix='uploads/')
for obj in response['Contents']:
    print(obj['Key'])

# Generar URL pre-firmada (temporal)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'uploads/file.jpg'},
    ExpiresIn=3600  # 1 hora
)
```

---

### 8.3 Resumen de Asignaciones

| Componente | Modelo | Servicio Específico | Justificación Clave |
|------------|--------|---------------------|---------------------|
| **Web App** | SaaS + CDN | S3 + CloudFront | Hosting estático global, zero-maintenance |
| **Mobile Backend** | PaaS | AWS Amplify | Backend especializado para móviles |
| **API Gateway** | PaaS | API Gateway | Gestionado, seguro, escalable |
| **Load Balancer** | PaaS | ALB | Alta disponibilidad automática |
| **API Layer** | PaaS | Elastic Beanstalk | Foco en código, auto-scaling |
| **Microservicios** | PaaS | ECS/EKS | Kubernetes gestionado |
| **Functions** | FaaS | Lambda | Event-driven, pay-per-execution |
| **Database** | PaaS | RDS | BD gestionada, backups automáticos |
| **File Storage** | IaaS | S3 | Object storage ilimitado |

### 8.4 Diagrama de Modelos de Servicio

**Representación Visual:**

![Distribución de Modelos de Servicio](../imagenes/modelo_servicios.png)

**Representación ASCII (texto):**

```
┌─────────────────────────────────────────────────┐
│         DISTRIBUCIÓN DE MODELOS                 │
└─────────────────────────────────────────────────┘

    SaaS (CDN)
    ┌──────────────┐
    │  CloudFront  │
    │   (Web App)  │
    └──────────────┘
           │
           ▼
    PaaS (API Gateway)
    ┌──────────────┐
    │ API Gateway  │
    └──────────────┘
           │
           ▼
    PaaS (Load Balancer)
    ┌──────────────┐
    │     ALB      │
    └──────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
PaaS (Backend)  PaaS (Containers)
┌──────────┐    ┌──────────┐
│Beanstalk │    │ ECS/EKS  │
└──────────┘    └──────────┘
     │               │
     └───────┬───────┘
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
   PaaS   FaaS   IaaS
 ┌─────┐ ┌────┐ ┌───┐
 │ RDS │ │Lambda│S3 │
 └─────┘ └────┘ └───┘
```

---

## 9. Conclusiones

### 9.1 Decisiones Arquitectónicas Clave

#### Enfoque Mayoritariamente PaaS
- ✅ **80% PaaS** para maximizar productividad
- ✅ **15% FaaS** para procesamiento event-driven
- ✅ **5% IaaS** solo para object storage

**Beneficios de este approach:**
- ⚡ **Time-to-market reducido**
- 🔧 **Mantenimiento mínimo**
- 💰 **Costos optimizados** (OpEx, pago por uso)
- 📈 **Escalabilidad automática**
- 🔒 **Seguridad gestionada**

#### Sin IaaS (VMs) en Compute
**Decisión:** Evitar EC2 y VMs tradicionales

**Justificación:**
- ❌ IaaS requiere gestionar OS, parches, seguridad
- ❌ Mayor complejidad operacional
- ❌ Escalado manual o semi-automático
- ✅ PaaS/FaaS cumplen todos los requisitos
- ✅ Equipo puede enfocarse en valor de negocio

### 9.2 Alineación con Objetivos del Proyecto

| Objetivo Original | Cómo lo Resolvemos |
|-------------------|-------------------|
| ❌ Problemas de escalabilidad | ✅ Auto-scaling en todos los componentes |
| ❌ Costos elevados | ✅ Modelo pay-per-use, sin servidores idle |
| ❌ Baja resiliencia | ✅ Alta disponibilidad multi-AZ, managed services |
| ❌ Modernización | ✅ Arquitectura cloud-native (microservicios, serverless) |

### 9.3 Próximos Pasos

En la **Lección 3** definiremos:
- ✅ Modelo de implementación (pública, privada, híbrida)
- ✅ Justificación del modelo elegido
- ✅ Consideraciones de seguridad y compliance

En la **Lección 4** aplicaremos:
- ✅ Principios de diseño arquitectónico
- ✅ Esquema conceptual detallado

En la **Lección 5** incorporaremos:
- ✅ Atributos de calidad (resiliencia, seguridad, escalabilidad)

---

## 📚 Referencias

- [AWS Service Models](https://aws.amazon.com/types-of-cloud-computing/)
- [Azure Service Models](https://azure.microsoft.com/overview/what-is-paas/)
- [Google Cloud Service Models](https://cloud.google.com/learn/what-is-iaas)
- [Martin Fowler - Microservices](https://martinfowler.com/articles/microservices.html)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

---

[← Volver: Lección 1](./Leccion_01_Fundamentos_Cloud.md) | [Siguiente: Lección 3 →](./Leccion_03_Modelos_Implementacion.md)
