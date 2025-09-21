"""
Utilidades comunes para el sistema de administración
"""
import streamlit as st
from datetime import datetime
import hashlib
import re

def generate_category_id(name: str) -> str:
    """Generar ID único para una categoría basado en el nombre"""
    # Convertir a minúsculas y reemplazar espacios con guiones
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
    slug = re.sub(r'\s+', '_', slug.strip())
    
    # Agregar timestamp para unicidad
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{slug}_{timestamp}"

def generate_work_id(name: str) -> str:
    """Generar ID único para un trabajo basado en el nombre"""
    # Convertir a minúsculas y reemplazar espacios con guiones
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    
    # Agregar timestamp para unicidad
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{slug}-{timestamp}"

def format_date(date_str: str) -> str:
    """Formatear fecha para mostrar en la interfaz"""
    if not date_str:
        return "N/A"
    
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime("%d/%m/%Y %H:%M")
    except:
        return date_str

def get_status_badge(status: str) -> str:
    """Obtener emoji para el estado"""
    status_emojis = {
        "active": "🟢",
        "paused": "⏸️", 
        "archived": "📁",
        "maintenance": "🔧"
    }
    return status_emojis.get(status, "❓")

def show_success_message(message: str):
    """Mostrar mensaje de éxito"""
    st.success(message)

def show_error_message(message: str):
    """Mostrar mensaje de error"""
    st.error(message)

def show_info_message(message: str):
    """Mostrar mensaje informativo"""
    st.info(message)

def validate_image_file(file) -> tuple[bool, str]:
    """Validar archivo de imagen"""
    if file is None:
        return False, "No se seleccionó archivo"
    
    # Verificar tipo de archivo
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if file.type not in allowed_types:
        return False, f"Tipo de archivo no permitido. Use: {', '.join(allowed_types)}"
    
    # Verificar tamaño (5MB máximo)
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        return False, "El archivo es muy grande. Máximo 5MB"
    
    return True, "Archivo válido"
