# 📸 Imágenes del Proyecto "Nube Sólida"

## Diagramas Requeridos

Este proyecto requiere **4 diagramas principales** que debes crear siguiendo la [GUIA_DIAGRAMAS.md](./GUIA_DIAGRAMAS.md):

### 1. 🏗️ arquitectura_conceptual.png

**Contenido:**
- Arquitectura completa Multi-AZ (us-east-1)
- Todos los servicios AWS (CloudFront, ALB, ECS, RDS, Lambda, S3, etc.)
- Flujos de red y seguridad
- VPC con subnets públicas/privadas
- Componentes de escalabilidad y resiliencia

**Vinculada en:**
- ✅ `/README.md` - Sección "Diagramas de Arquitectura"
- ✅ `/documentos/Documento_Integrador_Final.md` - Sección 7.1

**Tamaño recomendado:** 1920x1080 px
**Ver ejemplo en:** Lección 4, sección 6.1

---

### 2. 🔄 diagrama_cliente_servidor.png

**Contenido:**
- Separación clara de capas (Cliente, Servidor, Datos)
- Componentes de cada capa
- Flujos de comunicación entre capas
- APIs REST expuestas
- Protocolos utilizados (HTTPS, PostgreSQL, etc.)

**Vinculada en:**
- ✅ `/README.md` - Sección "Diagramas de Arquitectura"
- ✅ `/documentos/Leccion_04_Principios_Diseño.md` - Sección 6.2

**Tamaño recomendado:** 1600x1200 px
**Ver ejemplo en:** Lección 4, sección 6.2 (diagrama ASCII)

---

### 3. 📊 flujo_datos.png

**Contenido:**
- Recorrido completo de una petición (usuario → respuesta)
- Timeline con latencias por componente
- DNS → CloudFront → WAF → ALB → ECS → RDS
- Transformaciones de datos en cada paso
- Puntos de caché (CloudFront, Redis)
- Tiempos estimados por componente

**Vinculada en:**
- ✅ `/README.md` - Sección "Diagramas de Arquitectura"
- ✅ `/documentos/Documento_Integrador_Final.md` - Sección 7.2

**Tamaño recomendado:** 1800x1000 px (horizontal)
**Ver ejemplo en:** Lección 4, sección 6.3

---

### 4. 📈 modelo_servicios.png

**Contenido:**
- Distribución de modelos de servicio:
  - **PaaS (70%):** API Gateway, ALB, ECS, RDS
  - **FaaS (15%):** Lambda
  - **SaaS (10%):** CloudFront
  - **IaaS (5%):** S3
- Gráfico de torta o barras mostrando porcentajes
- Componentes específicos por cada modelo
- Justificación visual de cada modelo

**Vinculada en:**
- ✅ `/README.md` - Sección "Diagramas de Arquitectura"
- ✅ `/documentos/Leccion_02_Modelos_Servicio.md` - Sección 8.4

**Tamaño recomendado:** 1600x900 px
**Ver ejemplo en:** Lección 2, sección 8.4 (tabla de distribución)

---

## 🎨 Cómo Crear las Imágenes

### Opción 1: Draw.io (Recomendado)

1. Abre [Draw.io](https://app.diagrams.net/)
2. Sigue las instrucciones en [GUIA_DIAGRAMAS.md](./GUIA_DIAGRAMAS.md)
3. Usa los iconos de AWS del menú lateral
4. Exporta como PNG (300 DPI)

### Opción 2: Lucidchart

1. Abre [Lucidchart](https://www.lucidchart.com/)
2. Usa la plantilla "AWS Architecture"
3. Sigue la estructura de los diagramas ASCII en las lecciones
4. Exporta como PNG de alta resolución

### Opción 3: CloudCraft

1. Abre [CloudCraft](https://www.cloudcraft.co/)
2. Diseña la arquitectura en 3D (se ve muy profesional)
3. Exporta como PNG

---

## ✅ Checklist de Validación

Antes de considerar los diagramas completos, verifica:

- [ ] Las 4 imágenes están creadas
- [ ] Todas tienen nombres exactos (arquitectura_conceptual.png, etc.)
- [ ] Están guardadas en la carpeta `/imagenes/`
- [ ] Resolución mínima: 1600x900 px
- [ ] Formato PNG con fondo transparente o blanco
- [ ] Se ven claramente todos los textos y componentes
- [ ] Siguen el estilo profesional (no parecen hechos a mano)
- [ ] Incluyen leyendas y títulos
- [ ] Usan iconos oficiales de AWS

---

## 📂 Estructura Final de /imagenes/

```
imagenes/
├── README.md (este archivo)
├── GUIA_DIAGRAMAS.md (guía detallada)
├── arquitectura_conceptual.png 
├── diagrama_cliente_servidor.png 
├── flujo_datos.png
└── modelo_servicios.png 
```

---

## 🔗 Referencias Cruzadas

Cada imagen está referenciada en múltiples documentos para facilitar la navegación:

| Imagen | Documento 1 | Documento 2 |
|--------|-------------|-------------|
| arquitectura_conceptual.png | README.md | Documento_Integrador_Final.md |
| diagrama_cliente_servidor.png | README.md | Leccion_04_Principios_Diseño.md |
| flujo_datos.png | README.md | Documento_Integrador_Final.md |
| modelo_servicios.png | README.md | Leccion_02_Modelos_Servicio.md |

---

## 💡 Tips para Crear Diagramas Profesionales

1. **Usa colores consistentes:**
   - Azul para servicios de red (ALB, CloudFront)
   - Naranja para compute (ECS, Lambda)
   - Verde para datos (RDS, S3)
   - Rojo para seguridad (WAF, GuardDuty)

2. **Agrupa servicios relacionados:**
   - VPC con borde visible
   - Subnets claramente diferenciadas
   - Zonas de disponibilidad marcadas

3. **Usa flechas para indicar flujo:**
   - Flechas sólidas para flujo principal
   - Flechas punteadas para flujo opcional
   - Números en flechas para secuencia

4. **Incluye leyenda:**
   - Explica símbolos y colores
   - Agrega notas importantes
   - Indica escalas si aplica

---

## 🚀 Próximos Pasos

1. **Crear las 4 imágenes** usando Draw.io (la más rápida)
2. **Guardarlas** en esta carpeta con nombres exactos
3. **Verificar** que se vean correctamente en los documentos markdown
4. **Commit** y **push** a GitHub

```bash
# Después de crear las imágenes:
git add imagenes/*.png
git commit -m "docs: Add 4 architecture diagrams"
git push origin main
```
