# Data Science Admin

Sistema de administración para gestionar categorías y trabajos del Data Science Index.

## CRUDs Disponibles

### 1. CRUD de Categorías
- Crear, editar, archivar categorías
- Gestionar iconos y orden de visualización
- Tabla: `platform-partners-des.settings.works_categories`

### 2. CRUD de Trabajos
- Crear, editar, archivar trabajos
- Asignar a categorías existentes
- Tabla: `platform-partners-des.settings.works_index`

## Configuración

1. Instalar dependencias: `pip install -r requirements.txt`
2. Configurar variables de entorno para BigQuery
3. Ejecutar: `streamlit run admin_main.py`

## Base de Datos

- Categorías: `platform-partners-des.settings.works_categories`
- Trabajos: `platform-partners-des.settings.works_index`
