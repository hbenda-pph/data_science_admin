"""
Configuraciones del sistema de administración
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de BigQuery
BIGQUERY_PROJECT = "platform-partners-des"
BIGQUERY_DATASET = "settings"
BIGQUERY_CATEGORIES_TABLE = "works_categories"
BIGQUERY_WORKS_TABLE = "works_index"

# Configuración de Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Data Science Admin",
    "page_icon": "⚙️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuración de la aplicación
APP_CONFIG = {
    "title": "Data Science Admin",
    "subtitle": "Sistema de Administración - Categorías y Trabajos",
    "page_icon": "⚙️",
    "admin_password": os.getenv("ADMIN_PASSWORD", "admin123"),
    "max_image_size": 5 * 1024 * 1024,  # 5MB
    "allowed_image_types": ["jpg", "jpeg", "png", "gif"]
}

# Estados de trabajos
WORK_STATUS = {
    "ACTIVE": "active",
    "PAUSED": "paused", 
    "ARCHIVED": "archived",
    "MAINTENANCE": "maintenance"
}

# Iconos disponibles para categorías
CATEGORY_ICONS = [
    "📊", "📈", "📉", "📋", "📞", "💰", "👥", "🌡️", "📱", 
    "💻", "🔧", "📊", "📈", "🎯", "🚀", "⚡", "🔍", "📊"
]
