#Mesesario
Aplicación web fullstack para registrar y visualizar recuerdos mensuales con persistencia real en la nube.
Este proyecto no es un prototipo: es un sistema completo con frontend, backend, base de datos y almacenamiento externo, diseñado para resolver problemas reales de persistencia y manejo de archivos.

##Demo
Frontend: https://jessymanuel.netlify.app
Backend API: https://mesesario-backend.onrender.com/api/months

##Descripción
Mesesario permite registrar momentos importantes por mes mediante:
* Nombre del mes (ej. "Abril 2025")
* Descripción
* Imagen destacada
Cada registro se almacena en una base de datos externa y su imagen en un servicio de almacenamiento en la nube, asegurando persistencia real y disponibilidad.

##Arquitectura
Frontend (Netlify)
↓
Backend API (FastAPI en Render)
↓
PostgreSQL (Render)
↓
Cloudinary (Storage de imágenes)

##Stack Tecnológico
Frontend:
* HTML
* CSS
* JavaScript
Backend:
* Python
* FastAPI
* SQLAlchemy
Infraestructura:
* Render (API + PostgreSQL)
* Netlify (Frontend)
* Cloudinary (Gestión de imágenes)

##Características clave
* CRUD completo de registros mensuales
* Subida de imágenes a Cloudinary (no almacenamiento local)
* Persistencia real en PostgreSQL
* Eliminación sincronizada:
  * elimina registro en DB
  * elimina imagen en Cloudinary
* Comunicación frontend-backend vía API REST
* Deploy completo en producción

##  API
GET /api/months
→ Obtiene todos los meses
POST /api/months
→ Crea un nuevo registro con imagen
DELETE /api/months/{id}
→ Elimina el mes y su imagen asociada en la nube

## 🔐 Variables de entorno
DATABASE_URL=postgresql://...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

##Problema técnico resuelto
Problema:
Las imágenes se almacenaban localmente en el servidor, lo que provocaba pérdida de datos al reiniciar o redeployar.
Solución:
* Migración a Cloudinary para almacenamiento persistente
* Uso de URLs públicas para servir imágenes
* Implementación de eliminación real (DB + Cloudinary)
* Separación correcta entre backend y almacenamiento

##Estado del proyecto
✔ Sistema funcional en producción
✔ Arquitectura fullstack real
✔ Persistencia asegurada
✔ Manejo correcto de archivos en la nube

##Posibles mejoras
* Autenticación de usuarios
* Edición de registros
* Optimización de imágenes
* Mejoras en UX/UI
* Versionado de recuerdos

##Autor
Manuel Silva Madrid
Licenciatura en Ingeniería Ciencias de la Programación
Enfocado en backend, sistemas y desarrollo de software

##Enfoque
Este proyecto demuestra:
* Integración de múltiples servicios (API + DB + Storage)
* Resolución de problemas reales de persistencia
* Deploy completo de una arquitectura moderna
* Capacidad de llevar una idea a producción
