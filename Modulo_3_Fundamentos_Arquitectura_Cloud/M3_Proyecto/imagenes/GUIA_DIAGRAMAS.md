# 🎨 Guía para Crear Diagramas de Arquitectura

## Herramientas Recomendadas para Diagramas Profesionales

Esta guía te ayudará a crear los diagramas de arquitectura necesarios para el proyecto "Nube Sólida".

---

## 📊 Herramientas Recomendadas

### 1. **Draw.io / Diagrams.net** (RECOMENDADO)

**Por qué es la mejor opción:**
- ✅ Gratuito y open source
- ✅ Funciona en navegador (no requiere instalación)
- ✅ Tiene biblioteca de iconos AWS oficial
- ✅ Exporta a PNG, SVG, PDF
- ✅ Integración con GitHub

**Enlace:** https://app.diagrams.net/

#### Cómo usar Draw.io para AWS

1. Abre https://app.diagrams.net/
2. Click en "Create New Diagram"
3. Selecciona "Blank Diagram"
4. En el panel izquierdo, busca "AWS" o "AWS19"
5. Arrastra los iconos necesarios al canvas

**Biblioteca de iconos AWS:**
- `More Shapes` → buscar "AWS"
- `AWS19` → iconos oficiales más recientes

---

### 2. **Lucidchart**

**Características:**
- Interfaz intuitiva
- Colaboración en tiempo real
- Templates de arquitectura AWS

**Enlace:** https://www.lucidchart.com/

**Limitación:** Versión gratuita limitada

---

### 3. **CloudCraft**

**Especializado en AWS:**
- Diagramas 3D de arquitectura AWS
- Calcula costos automáticamente
- Muy visual y profesional

**Enlace:** https://www.cloudcraft.co/

**Limitación:** Requiere cuenta (hay free tier)

---

## 🎨 Diagramas Requeridos para el Proyecto

### Diagrama 1: Arquitectura Conceptual Completa

**Nombre del archivo:** `arquitectura_conceptual.png`

**Elementos a incluir:**

```
┌─────────────────────────────────────────────┐
│           CAPA DE USUARIOS                  │
│  [Icon] Usuario Web                         │
│  [Icon] Usuario Móvil                       │
│  [Icon] Usuario API                         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           CAPA DE EDGE                      │
│  [Icon] Route 53 (DNS)                      │
│  [Icon] CloudFront (CDN)                    │
│  [Icon] AWS WAF                             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│     VPC (Virtual Private Cloud)             │
│  ┌───────────────────────────────────────┐  │
│  │   PUBLIC SUBNET                       │  │
│  │   [Icon] Application Load Balancer    │  │
│  │   [Icon] NAT Gateway                  │  │
│  └───────────────────────────────────────┘  │
│                    ↓                        │
│  ┌───────────────────────────────────────┐  │
│  │   PRIVATE SUBNET (Multi-AZ)           │  │
│  │   ┌─────────────┐  ┌─────────────┐  │  │
│  │   │ ECS Fargate │  │ ECS Fargate │  │  │
│  │   │   (AZ-A)    │  │   (AZ-B)    │  │  │
│  │   └─────────────┘  └─────────────┘  │  │
│  │   ┌─────────────────────────────┐  │  │
│  │   │  Lambda Functions           │  │  │
│  │   └─────────────────────────────┘  │  │
│  │   ┌─────────────┐  ┌─────────────┐  │  │
│  │   │ RDS Primary │  │RDS Standby  │  │  │
│  │   │   (AZ-A)    │  │   (AZ-B)    │  │  │
│  │   └─────────────┘  └─────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           CAPA DE STORAGE                   │
│  [Icon] S3 (Object Storage)                 │
│  [Icon] DynamoDB (opcional)                 │
└─────────────────────────────────────────────┘
```

**Iconos AWS a usar:**
- Route 53 (DNS)
- CloudFront (CDN)
- AWS WAF & Shield
- VPC
- Application Load Balancer
- ECS / Fargate
- Lambda
- RDS (PostgreSQL)
- S3
- NAT Gateway

---

### Diagrama 2: Modelo Cliente-Servidor

**Nombre del archivo:** `diagrama_cliente_servidor.png`

**Elementos:**

```
CLIENTE                      SERVIDOR
┌──────────────┐            ┌──────────────────┐
│              │            │                  │
│  Web Browser │───HTTP───→│  API Gateway     │
│  (React App) │            │                  │
│              │            └──────────────────┘
└──────────────┘                     ↓
                            ┌──────────────────┐
┌──────────────┐            │                  │
│              │            │  Load Balancer   │
│ Mobile App   │───HTTPS──→│                  │
│ (React       │            └──────────────────┘
│  Native)     │                     ↓
└──────────────┘            ┌──────────────────┐
                            │  Application     │
┌──────────────┐            │  Servers         │
│              │            │  (ECS Fargate)   │
│  External    │───API────→│                  │
│  Services    │            └──────────────────┘
│              │                     ↓
└──────────────┘            ┌──────────────────┐
                            │                  │
                            │  Database        │
                            │  (RDS)           │
                            │                  │
                            └──────────────────┘
```

---

### Diagrama 3: Flujo de Datos

**Nombre del archivo:** `flujo_datos.png`

**Secuencia de flujo:**

```
1. Usuario hace request
   ↓
2. DNS (Route 53) resuelve
   ↓
3. CDN (CloudFront) cachea o forward
   ↓
4. WAF valida seguridad
   ↓
5. Load Balancer distribuye
   ↓
6. ECS Fargate procesa
   ├→ Consulta RDS (lectura)
   ├→ Escribe en S3 (archivos)
   └→ Invoca Lambda (async)
   ↓
7. Respuesta al usuario
   ↓
8. CloudWatch registra logs
```

---

### Diagrama 4: Modelo de Servicios (IaaS/PaaS/SaaS/FaaS)

**Nombre del archivo:** `modelo_servicios.png`

**Representación visual:**

```
┌─────────────────────────────────────────┐
│           SaaS (10%)                    │
│  ┌────────────────────────────────┐    │
│  │  CloudFront CDN                │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           PaaS (70%)                    │
│  ┌────────────────────────────────┐    │
│  │  API Gateway                   │    │
│  │  Elastic Beanstalk / ECS       │    │
│  │  RDS (Database)                │    │
│  │  Load Balancer                 │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           FaaS (15%)                    │
│  ┌────────────────────────────────┐    │
│  │  Lambda Functions              │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│           IaaS (5%)                     │
│  ┌────────────────────────────────┐    │
│  │  S3 (Object Storage)           │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## 🎨 Mejores Prácticas para Diagramas Profesionales

### Principios de Diseño

1. **Claridad sobre Complejidad**
   - Evita saturar el diagrama
   - Un diagrama = una historia
   - Si es muy complejo, dividir en múltiples diagramas

2. **Consistencia de Iconos**
   - Usa siempre iconos oficiales de AWS
   - Mantén el mismo estilo de iconos en todo el diagrama
   - No mezcles estilos diferentes

3. **Flujo de Arriba hacia Abajo**
   - Usuario en la parte superior
   - Datos/Storage en la parte inferior
   - Flujo natural de lectura

4. **Colores Significativos**
   - Verde: componentes healthy/activos
   - Rojo: problemas o alertas
   - Azul: componentes de red
   - Naranja: procesamiento/compute

5. **Etiquetas Claras**
   - Nombre del servicio
   - Tipo de instancia (si aplica)
   - Availability Zone

### Elementos Visuales

**Flechas:**
- Línea sólida → Flujo principal de datos
- Línea punteada → Flujo secundario o condicional
- Flecha bidireccional → Comunicación síncrona
- Flecha unidireccional → Comunicación asíncrona

**Agrupaciones:**
- Rectángulo con borde → VPC
- Rectángulo con borde punteado → Subnet
- Rectángulo con sombra → Availability Zone
- Círculo → Security Group

---

## 📐 Template de Diagrama en Draw.io

### Pasos para crear diagrama profesional:

1. **Configuración del Canvas**
   ```
   Tamaño: A4 Landscape (297 x 210 mm)
   o
   Custom: 1920 x 1080 px (para pantalla)
   ```

2. **Agregar Biblioteca AWS**
   - Click en `More Shapes`
   - Buscar "AWS"
   - Seleccionar "AWS19" (más reciente)
   - Click "Apply"

3. **Estructura Base**
   ```
   Capa 1 (Background):
     └─ Rectángulo grande para VPC
   
   Capa 2 (Network):
     └─ Rectángulos para Subnets (público/privado)
   
   Capa 3 (Compute):
     └─ Iconos de servicios (ECS, Lambda, RDS)
   
   Capa 4 (Connections):
     └─ Flechas y líneas de flujo
   
   Capa 5 (Labels):
     └─ Textos y descripciones
   ```

4. **Paleta de Colores Recomendada**
   ```
   VPC Border:        #232F3E (AWS Dark)
   Public Subnet:     #D1F2EB (Light Teal)
   Private Subnet:    #FEF9E7 (Light Yellow)
   Security Group:    #E8F8F5 (Light Mint)
   Connections:       #3498DB (Blue)
   Text Primary:      #2C3E50 (Dark Gray)
   Text Secondary:    #7F8C8D (Light Gray)
   ```

5. **Exportar**
   - File → Export As → PNG
   - Opciones recomendadas:
     - Zoom: 100%
     - Border: 20px
     - Transparent Background: No
     - Include a copy of my diagram: Yes (para editar después)

---

## 🖼️ Iconos AWS Principales

### Compute
- **EC2:** Compute/Amazon EC2
- **Lambda:** Compute/AWS Lambda
- **ECS:** Containers/Amazon ECS
- **Fargate:** Containers/AWS Fargate

### Network & Content Delivery
- **VPC:** Network & Content Delivery/Amazon VPC
- **ELB:** Network & Content Delivery/Elastic Load Balancing
- **CloudFront:** Network & Content Delivery/Amazon CloudFront
- **Route 53:** Network & Content Delivery/Amazon Route 53
- **API Gateway:** Network & Content Delivery/Amazon API Gateway

### Database
- **RDS:** Database/Amazon RDS
- **DynamoDB:** Database/Amazon DynamoDB

### Storage
- **S3:** Storage/Amazon S3
- **EBS:** Storage/Amazon EBS

### Security
- **IAM:** Security, Identity & Compliance/AWS IAM
- **WAF:** Security, Identity & Compliance/AWS WAF
- **Secrets Manager:** Security, Identity & Compliance/AWS Secrets Manager

### Management
- **CloudWatch:** Management & Governance/Amazon CloudWatch
- **CloudTrail:** Management & Governance/AWS CloudTrail

---

## 💾 Guardado de Diagramas

### Ubicación en el Proyecto

```
M3_Proyecto/
└── imagenes/
    ├── arquitectura_conceptual.png
    ├── arquitectura_conceptual.drawio (editable)
    ├── diagrama_cliente_servidor.png
    ├── diagrama_cliente_servidor.drawio
    ├── flujo_datos.png
    ├── flujo_datos.drawio
    └── modelo_servicios.png
```

### Formatos a Guardar

1. **PNG** (para README y documentación)
   - Resolución: 300 DPI
   - Compresión: Alta calidad

2. **.drawio** (para futuras ediciones)
   - Incluir siempre el source file
   - Permite modificaciones posteriores

3. **SVG** (opcional, para web)
   - Formato vectorial
   - Escala sin perder calidad

---

## 📚 Recursos Adicionales

### Templates y Ejemplos

- [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)
- [AWS Architecture Diagrams](https://aws.amazon.com/architecture/)
- [Draw.io AWS Examples](https://www.diagrams.net/blog/aws-diagrams)

### Videos Tutorial

- [How to Create AWS Architecture Diagrams](https://www.youtube.com/watch?v=0vTxKD6nnYs)
- [Draw.io for AWS](https://www.youtube.com/results?search_query=drawio+aws)

### Checklist de Calidad

Antes de finalizar un diagrama, verifica:

- [ ] Usa iconos oficiales de AWS
- [ ] Todos los componentes están etiquetados
- [ ] El flujo de datos es claro
- [ ] Hay leyenda si hay colores/símbolos especiales
- [ ] El tamaño es legible (no muy pequeño)
- [ ] Incluye título del diagrama
- [ ] Incluye versión y fecha
- [ ] Exportado en alta resolución (300 DPI)
- [ ] Source file (.drawio) guardado

---

## 🎓 Tips Profesionales

1. **Versiona tus Diagramas**
   ```
   arquitectura_conceptual_v1.0.png
   arquitectura_conceptual_v1.1.png
   ```

2. **Incluye Metadata**
   ```
   Título: Arquitectura Cloud - Nube Sólida
   Versión: 1.0
   Fecha: Enero 2026
   Autor: [Tu Nombre]
   ```

3. **Documenta Cambios**
   - Mantén un changelog de versiones
   - Explica por qué cambiaste algo

4. **Solicita Feedback**
   - Comparte con colegas
   - Pregunta si el diagrama es claro
   - Itera basado en feedback

---

<div align="center">

**¡Con esta guía podrás crear diagramas profesionales para tu portafolio!**

</div>
