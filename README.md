# Mesesario

Aplicación web fullstack para registrar y visualizar recuerdos mensuales con persistencia real en la nube.

> Sistema completo con frontend, backend, base de datos y almacenamiento externo. No es un prototipo.

## Demo

- Frontend: https://mesesario-beta.vercel.app  
- Backend API: https://mesesario-backend.onrender.com/api/months  

## Descripción

Mesesario permite registrar momentos importantes mes a mes con soporte para **dos recuerdos por mes (uno por persona)**:

- Nombre del mes (ej. "Abril 2025")
- Recuerdo 1 (descripción + imagen)
- Recuerdo 2 (descripción + imagen)
- Opción de destacar un mes

Permite construir una **línea del tiempo emocional compartida**.


## Arquitectura

Frontend (Vercel)  
↓  
Backend API (FastAPI - Render)  
↓  
PostgreSQL (Render)  
↓  
Cloudinary (Storage de imágenes)

## Stack Tecnológico

### Frontend
- HTML
- CSS (Responsive)
- JavaScript (Fetch API)

### Backend
- Python
- FastAPI
- SQLAlchemy

### Infraestructura
- Render (API + PostgreSQL)
- Vercel (Frontend)
- Cloudinary (imágenes)

## Características

- ✔ CRUD completo de meses
- ✔ Soporte para dos recuerdos por mes
- ✔ Subida de imágenes a Cloudinary
- ✔ Persistencia real en PostgreSQL
- ✔ Eliminación sincronizada (DB + Cloudinary)
- ✔ API REST desacoplada
- ✔ Deploy en producción
- ✔ Diseño responsive

## API

### GET meses
GET /api/months

### POST crear mes
POST /api/months

Form-data:
- month_label
- description_1
- description_2
- image_1 (opcional)
- image_2 (opcional)
- is_featured

### DELETE mes
DELETE /api/months/{id}

## Variables de entorno

DATABASE_URL=postgresql://...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

## Problema resuelto

### Problema
Las imágenes se almacenaban localmente, lo que provocaba pérdida de datos al redeployar.

### Solución
- Uso de Cloudinary
- URLs públicas
- Eliminación sincronizada
- Separación backend / storage

## Estado

- ✔ Funcional en producción  
- ✔ Persistencia asegurada  
- ✔ Arquitectura fullstack real  
- ✔ Manejo correcto de archivos  

## Mejoras futuras

- Autenticación
- Edición de recuerdos
- Mejor UX/UI
- App móvil
- Timeline animado

## Autor

Manuel Silva Madrid
Licenciaura en Ingeniería en Ciencias de la Computación (BUAP)  
Enfocado en backend y desarrollo de software  
