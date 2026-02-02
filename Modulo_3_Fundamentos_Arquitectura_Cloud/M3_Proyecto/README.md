# Proyecto: Nube Sólida

## Evaluación del Módulo 3 - Fundamentos de la Arquitectura Cloud

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/tu-usuario/fundamentos_arquitectura_cloud_portafolio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Situación Inicial](#-situación-inicial)
- [Objetivos](#-objetivos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos y Requerimientos](#-requisitos-y-requerimientos)
- [Desarrollo por Lecciones](#-desarrollo-por-lecciones)
- [Entregables](#-entregables)
- [Tecnologías y Herramientas](#-tecnologías-y-herramientas)
- [Referencias](#-referencias)

---

## 🎯 Descripción del Proyecto

**Nube Sólida** es un proyecto académico enfocado en el diseño conceptual de una arquitectura cloud empresarial robusta, escalable y segura. Este proyecto integra los fundamentos de la computación en la nube, aplicando principios de diseño arquitectónico modernos basados en el modelo cliente-servidor.

El proyecto se desarrolla a través de **5 lecciones progresivas**, cada una construyendo sobre los fundamentos de la anterior, culminando en un diseño arquitectónico completo y documentado profesionalmente.

---

## 📍 Situación Inicial

### Contexto Empresarial

**Unidad Solicitante:** Área de Infraestructura y Seguridad de una empresa de tecnología

### Problemática

La organización está atravesando un proceso crítico de **migración hacia la nube** para modernizar sus servicios y mejorar la disponibilidad de sus aplicaciones.

#### Desafíos Actuales:
- ❌ **Problemas de escalabilidad** en las soluciones existentes
- ❌ **Costos operativos elevados** 
- ❌ **Baja resiliencia ante fallos** del sistema
- ❌ **Infraestructura on-premise obsoleta**

### Solicitud

La dirección técnica ha solicitado al equipo de arquitectura elaborar un **diseño conceptual de arquitectura en la nube** que contemple:
- Principios fundamentales del modelo cliente-servidor
- Selección apropiada de servicios cloud
- Atributos de calidad: seguridad, escalabilidad y resiliencia

---

## 🎯 Objetivos

### Objetivo Principal

Desarrollar un **diseño conceptual de arquitectura en la nube** que integre:
- Fundamentos de la computación cloud
- Principios de diseño arquitectónico
- Atributos clave: escalabilidad, resiliencia y seguridad

### Objetivos Específicos

1. **Comprender** los fundamentos de la computación en la nube
2. **Seleccionar** modelos de servicio apropiados (IaaS, PaaS, SaaS, FaaS)
3. **Justificar** el modelo de implementación (pública, privada o híbrida)
4. **Diseñar** una arquitectura cliente-servidor robusta
5. **Incorporar** atributos de calidad en el diseño
6. **Documentar** todas las decisiones arquitectónicas

---

## 📁 Estructura del Proyecto

```
M3_Proyecto/
│
├── README.md                          # Este archivo
│
├── documentos/                        # Documentación técnica
│   ├── Leccion_01_Fundamentos_Cloud.md
│   ├── Leccion_02_Modelos_Servicio.md
│   ├── Leccion_03_Modelos_Implementacion.md
│   ├── Leccion_04_Principios_Diseño.md
│   ├── Leccion_05_Atributos_Calidad.md
│   └── Documento_Integrador_Final.md
│
├── codigo/                            # Ejemplos de código y configuración
│   ├── terraform/                     # IaC - Infraestructura como código
│   ├── kubernetes/                    # Configuraciones K8s
│   └── scripts/                       # Scripts de automatización
│
└── imagenes/                          # Diagramas y recursos visuales
    ├── arquitectura_conceptual.png
    ├── diagrama_cliente_servidor.png
    ├── flujo_datos.png
    └── modelo_servicios.png
```

---

## 🔧 Requisitos y Requerimientos

### Requerimientos Generales

- ✅ Comprensión y aplicación de fundamentos de computación en la nube
- ✅ Aplicación de principios de diseño arquitectónico:
  - Modularidad
  - Desacoplamiento
  - Resiliencia
  - Escalabilidad
  - Seguridad
- ✅ Integración del modelo cliente-servidor como base estructural
- ✅ Justificación clara de cada decisión arquitectónica

### Requerimientos Técnicos Específicos

#### 1. Modelos de Servicio
- Definición del modelo más adecuado para cada componente
- Comparativa: IaaS, PaaS, SaaS, FaaS
- Justificación técnica de selección

#### 2. Modelo de Implementación
- Selección entre: Pública, Privada o Híbrida
- Análisis de ventajas y desventajas
- Justificación basada en requisitos del negocio

#### 3. Diseño Conceptual Detallado
- Capas de cliente y servidor
- Atributos de calidad incorporados
- Flujos de datos y servicios utilizados
- Documentación técnica completa

---

## 📚 Desarrollo por Lecciones

### [Lección 1: Introducción a la Computación en la Nube](./documentos/Leccion_01_Fundamentos_Cloud.md)

**🎯 Objetivo:** Comprender los conceptos fundamentales de la computación en la nube

**📝 Entregables:**
- Informe sobre fundamentos y características de cloud computing
- Análisis de modelos de despliegue
- Comparativa de proveedores cloud principales

[Ver documento completo →](./documentos/Leccion_01_Fundamentos_Cloud.md)

---

### [Lección 2: Modelos de Servicio en la Nube](./documentos/Leccion_02_Modelos_Servicio.md)

**🎯 Objetivo:** Seleccionar y justificar modelos de servicio para cada componente

**📝 Entregables:**
- Informe técnico de análisis de modelos (IaaS, PaaS, SaaS, FaaS)
- Asignación de modelos a componentes
- Justificación técnica de decisiones

[Ver documento completo →](./documentos/Leccion_02_Modelos_Servicio.md)

---

### [Lección 3: Modelos de Implementación](./documentos/Leccion_03_Modelos_Implementacion.md)

**🎯 Objetivo:** Determinar el modelo de implementación óptimo

**📝 Entregables:**
- Análisis comparativo de modelos (público, privado, híbrido)
- Selección del modelo para la arquitectura
- Justificación considerando seguridad, costos y flexibilidad

[Ver documento completo →](./documentos/Leccion_03_Modelos_Implementacion.md)

---

### [Lección 4: Principios de Diseño Arquitectónico](./documentos/Leccion_04_Principios_Diseño.md)

**🎯 Objetivo:** Aplicar principios fundamentales de diseño arquitectónico

**📝 Entregables:**
- Esquema conceptual de arquitectura cliente-servidor
- Aplicación de principios de modularidad y desacoplamiento
- Documentación de decisiones de diseño

[Ver documento completo →](./documentos/Leccion_04_Principios_Diseño.md)

---

### [Lección 5: Atributos de Calidad](./documentos/Leccion_05_Atributos_Calidad.md)

**🎯 Objetivo:** Incorporar atributos de calidad en la arquitectura

**📝 Entregables:**
- Estrategias de resiliencia y tolerancia a fallos
- Medidas de seguridad implementadas
- Mecanismos de escalabilidad
- Documentación de integración de atributos

[Ver documento completo →](./documentos/Leccion_05_Atributos_Calidad.md)

---

## ✅ Entregables

### Documento Integrador Final

El [Documento Integrador](./documentos/Documento_Integrador_Final.md) consolida todos los informes y diagramas elaborados durante las 5 lecciones.

**Contenido:**
- ✅ Resumen ejecutivo del proyecto
- ✅ Fundamentos de computación en la nube aplicados
- ✅ Justificación de modelos de servicio seleccionados
- ✅ Justificación del modelo de implementación
- ✅ Diseño arquitectónico completo
- ✅ Principios de diseño aplicados
- ✅ Atributos de calidad incorporados
- ✅ Conclusiones y recomendaciones

### Diagramas de Arquitectura

#### 1. Arquitectura Conceptual Completa

![Arquitectura Cloud - Nube Sólida](./imagenes/arquitectura_conceptual.png)

**Muestra:**
- Arquitectura completa Multi-AZ
- Todos los servicios AWS utilizados
- Flujos de red y seguridad
- Componentes de escalabilidad y resiliencia

#### 2. Modelo Cliente-Servidor

![Modelo Cliente-Servidor](./imagenes/diagrama_cliente_servidor.png)

**Muestra:**
- Separación de capas (cliente, servidor, datos)
- Componentes de cada capa
- Comunicación entre capas
- APIs REST expuestas

#### 3. Flujo de Datos

![Flujo de Datos End-to-End](./imagenes/flujo_datos.png)

**Muestra:**
- Recorrido completo de una petición
- Latencias por componente
- Transformaciones de datos
- Puntos de caché

#### 4. Distribución de Modelos de Servicio

![Modelos de Servicio](./imagenes/modelo_servicios.png)

**Muestra:**
- Distribución PaaS (70%), FaaS (15%), SaaS (10%), IaaS (5%)
- Componentes por modelo
- Justificación de cada modelo
- Responsabilidad compartida

> 📌 **Nota:** Estos diagramas fueron creados siguiendo la [Guía de Diagramas](./imagenes/GUIA_DIAGRAMAS.md) incluida en el proyecto.

---

## 🛠️ Tecnologías y Herramientas

### Proveedores Cloud Analizados

- **Amazon Web Services (AWS)**
- **Google Cloud Platform (GCP)**
- **Microsoft Azure**

### Herramientas de Diseño

- **Draw.io / Diagrams.net** - Diagramas arquitectónicos
- **Lucidchart** - Modelado de arquitectura
- **PlantUML** - Diagramas como código

### Infraestructura como Código (IaC)

- **Terraform** - Provisión de infraestructura
- **CloudFormation** - AWS específico
- **ARM Templates** - Azure específico

### Contenedores y Orquestación

- **Docker** - Contenerización
- **Kubernetes** - Orquestación de contenedores
- **Helm** - Gestión de aplicaciones K8s

---

## 📖 Referencias

### Documentación Oficial

- [AWS - Documentación Oficial](https://docs.aws.amazon.com/)
- [Google Cloud - Documentación Oficial](https://cloud.google.com/docs)
- [Microsoft Azure - Documentación Oficial](https://docs.microsoft.com/azure/)

### Recursos de Aprendizaje

- [Get Started Architecting on AWS](https://aws.amazon.com/architecture/)
- [¿Qué es la arquitectura en la nube?](https://aws.amazon.com/what-is/cloud-architecture/)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Azure Architecture Center](https://docs.microsoft.com/azure/architecture/)

### Frameworks y Buenas Prácticas

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Microsoft Azure Well-Architected Framework](https://docs.microsoft.com/azure/architecture/framework/)

---

## 🎓 Criterios de Evaluación

### Aspectos Técnicos (40%)

- ✓ Aplicación correcta de principios de computación en la nube
- ✓ Coherencia en selección de modelos de servicio
- ✓ Justificación técnica de modelo de implementación
- ✓ Integración adecuada del modelo cliente-servidor

### Aspectos Estructurales (30%)

- ✓ Claridad y solidez del diseño conceptual
- ✓ Calidad de diagramas arquitectónicos
- ✓ Documentación técnica completa
- ✓ Profesionalismo en presentación

### Aspectos de Performance (30%)

- ✓ Enfoque en escalabilidad
- ✓ Estrategias de resiliencia implementadas
- ✓ Aplicación de buenas prácticas de seguridad
- ✓ Consistencia entre etapas del proyecto

---

[🏠 Índice Principal](../../README.md) | [📚 Volver al Módulo](../README.md) | [← Actividad Anterior](../M3_AE5_Atributos_Calidad/README.md) | [Actividad Siguiente →](../../Modulo_4_Fundamentos_Tecnologia_Cloud/M4_AE1_Almacenamiento/README.md)

---


