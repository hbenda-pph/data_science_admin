"""
Sistema de administración principal - CRUD de Categorías y Trabajos
"""
import streamlit as st
import sys
import os

# Agregar el directorio shared al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from database import CategoriesDatabase, WorksDatabase
from config import APP_CONFIG, WORK_STATUS, CATEGORY_ICONS
from utils import generate_category_id, generate_work_id, format_date, get_status_badge, show_success_message, show_error_message

# Configuración de la página
st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon=APP_CONFIG["page_icon"],
    layout="wide"
)

def check_admin_access():
    """Verificar acceso de administrador"""
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        st.title("🔐 Acceso de Administrador")
        
        password = st.text_input("Contraseña:", type="password")
        if st.button("Ingresar"):
            if password == APP_CONFIG["admin_password"]:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        
        st.stop()

def main():
    """Función principal de administración"""
    check_admin_access()
    
    st.title("⚙️ Data Science Admin")
    st.markdown("*Sistema de Administración - Categorías y Trabajos*")
    st.divider()
    
    # Tabs principales
    tab1, tab2 = st.tabs(["📂 Gestión de Categorías", "📋 Gestión de Trabajos"])
    
    with tab1:
        show_categories_management()
    
    with tab2:
        show_works_management()

def show_categories_management():
    """Gestión de categorías"""
    st.subheader("📂 Gestión de Categorías")
    
    # Subtabs para categorías
    cat_tab1, cat_tab2, cat_tab3 = st.tabs(["📋 Ver Categorías", "➕ Agregar Categoría", "✏️ Editar Categoría"])
    
    with cat_tab1:
        show_categories_list()
    
    with cat_tab2:
        show_add_category_form()
    
    with cat_tab3:
        show_edit_category_form()

def show_categories_list():
    """Mostrar lista de categorías"""
    try:
        db = CategoriesDatabase()
        categories_df = db.get_all_categories()
        
        if categories_df.empty:
            st.info("No hay categorías registradas.")
            return
        
        st.subheader("📋 Lista de Categorías")
        
        # Mostrar tabla
        display_df = categories_df[['category_name', 'category_icon', 'display_order', 'created_date']].copy()
        display_df['created_date'] = display_df['created_date'].apply(format_date)
        
        st.dataframe(display_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al cargar categorías: {str(e)}")

def show_add_category_form():
    """Formulario para agregar nueva categoría"""
    st.subheader("➕ Agregar Nueva Categoría")
    
    with st.form("add_category_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category_name = st.text_input("Nombre de la categoría *")
            category_icon = st.selectbox("Icono", CATEGORY_ICONS, index=0)
        
        with col2:
            display_order = st.number_input("Orden de visualización", min_value=1, value=999)
        
        submitted = st.form_submit_button("Agregar Categoría")
        
        if submitted:
            if not category_name:
                st.error("Por favor complete el nombre de la categoría")
            else:
                try:
                    # Generar ID único
                    category_id = generate_category_id(category_name)
                    
                    # Preparar datos para inserción
                    category_data = {
                        "category_id": category_id,
                        "category_name": category_name,
                        "category_icon": category_icon,
                        "display_order": display_order
                    }
                    
                    # Insertar en BigQuery
                    db = CategoriesDatabase()
                    if db.create_category(category_data):
                        st.success(f"✅ Categoría '{category_name}' creada exitosamente")
                        st.rerun()
                    else:
                        st.error("❌ Error al crear la categoría en BigQuery")
                    
                except Exception as e:
                    st.error(f"Error al crear categoría: {str(e)}")

def show_edit_category_form():
    """Formulario para editar categoría existente"""
    st.subheader("✏️ Editar Categoría Existente")
    
    try:
        db = CategoriesDatabase()
        categories_df = db.get_all_categories()
        
        if categories_df.empty:
            st.info("No hay categorías para editar.")
            return
        
        # Selector de categoría
        category_options = {row['category_name']: row['category_id'] 
                          for _, row in categories_df.iterrows()}
        
        selected_category_name = st.selectbox("Seleccionar categoría a editar:", list(category_options.keys()))
        selected_category_id = category_options[selected_category_name]
        
        # Obtener datos de la categoría seleccionada
        category_data = db.get_category_by_id(selected_category_id)
        
        if category_data:
            with st.form("edit_category_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    category_name = st.text_input("Nombre de la categoría *", value=category_data['category_name'])
                    category_icon = st.selectbox("Icono", CATEGORY_ICONS, 
                                               index=CATEGORY_ICONS.index(category_data.get('category_icon', '📊')))
                
                with col2:
                    display_order = st.number_input("Orden de visualización", 
                                                  min_value=1, 
                                                  value=category_data.get('display_order', 999))
                
                col1, col2 = st.columns(2)
                with col1:
                    update_submitted = st.form_submit_button("💾 Actualizar Categoría")
                with col2:
                    delete_submitted = st.form_submit_button("🗑️ Archivar Categoría", type="secondary")
                
                if update_submitted:
                    if not category_name:
                        st.error("Por favor complete el nombre de la categoría")
                    else:
                        try:
                            update_data = {
                                "category_name": category_name,
                                "category_icon": category_icon,
                                "display_order": display_order
                            }
                            
                            if db.update_category(selected_category_id, update_data):
                                st.success(f"✅ Categoría '{category_name}' actualizada exitosamente")
                                st.rerun()
                            else:
                                st.error("❌ Error al actualizar la categoría")
                                
                        except Exception as e:
                            st.error(f"Error al actualizar categoría: {str(e)}")
                
                if delete_submitted:
                    try:
                        if db.archive_category(selected_category_id):
                            st.success(f"✅ Categoría '{category_name}' archivada exitosamente")
                            st.rerun()
                        else:
                            st.error("❌ Error al archivar la categoría")
                    except Exception as e:
                        st.error(f"Error al archivar categoría: {str(e)}")
        
    except Exception as e:
        st.error(f"Error al cargar categorías: {str(e)}")

def show_works_management():
    """Gestión de trabajos"""
    st.subheader("📋 Gestión de Trabajos")
    
    # Subtabs para trabajos
    work_tab1, work_tab2, work_tab3 = st.tabs(["📋 Ver Trabajos", "➕ Agregar Trabajo", "✏️ Editar Trabajo"])
    
    with work_tab1:
        show_works_list()
    
    with work_tab2:
        show_add_work_form()
    
    with work_tab3:
        show_edit_work_form()

def show_works_list():
    """Mostrar lista de trabajos"""
    try:
        db = WorksDatabase()
        works_df = db.get_all_works()
        
        if works_df.empty:
            st.info("No hay trabajos registrados.")
            return
        
        st.subheader("📋 Lista de Trabajos")
        
        # Mostrar tabla
        display_df = works_df[['work_name', 'category', 'status', 'version', 'created_date']].copy()
        display_df['created_date'] = display_df['created_date'].apply(format_date)
        
        st.dataframe(display_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al cargar trabajos: {str(e)}")

def show_add_work_form():
    """Formulario para agregar nuevo trabajo"""
    st.subheader("➕ Agregar Nuevo Trabajo")
    
    # Obtener categorías disponibles
    try:
        cat_db = CategoriesDatabase()
        categories_df = cat_db.get_all_categories()
        
        if categories_df.empty:
            st.warning("No hay categorías disponibles. Crea categorías primero.")
            return
        
        category_options = {row['category_name']: row['category_id'] 
                          for _, row in categories_df.iterrows()}
        
        with st.form("add_work_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                work_name = st.text_input("Nombre del trabajo *")
                category = st.selectbox("Categoría *", list(category_options.keys()))
                subcategory = st.text_input("Subcategoría")
                version = st.text_input("Versión *", value="1.0")
            
            with col2:
                status = st.selectbox("Estado *", list(WORK_STATUS.values()))
                streamlit_page = st.text_input("Archivo Streamlit *", placeholder="categories/calls_analysis/individual_companies.py")
                image_file = st.file_uploader("Imagen preview", type=['jpg', 'jpeg', 'png', 'gif'])
            
            description = st.text_area("Descripción")
            short_description = st.text_area("Descripción corta (para el índice)")
            notes = st.text_area("Notas internas")
            
            submitted = st.form_submit_button("Agregar Trabajo")
            
            if submitted:
                if not work_name or not version or not streamlit_page:
                    st.error("Por favor complete todos los campos obligatorios (*)")
                else:
                    try:
                        # Generar ID único
                        work_id = generate_work_id(work_name)
                        work_slug = work_id
                        
                        # Obtener category_id
                        category_id = category_options[category]
                        
                        # Preparar datos para inserción
                        work_data = {
                            "work_id": work_id,
                            "work_name": work_name,
                            "work_slug": work_slug,
                            "category": category_id,
                            "subcategory": subcategory,
                            "status": status,
                            "version": version,
                            "is_latest": True,
                            "description": description,
                            "short_description": short_description,
                            "streamlit_page": streamlit_page,
                            "notes": notes,
                            "tags": []
                        }
                        
                        # Insertar en BigQuery
                        db = WorksDatabase()
                        if db.create_work(work_data):
                            st.success(f"✅ Trabajo '{work_name}' creado exitosamente con ID: {work_id}")
                            st.rerun()
                        else:
                            st.error("❌ Error al crear el trabajo en BigQuery")
                        
                    except Exception as e:
                        st.error(f"Error al crear trabajo: {str(e)}")
        
    except Exception as e:
        st.error(f"Error al cargar categorías: {str(e)}")

def show_edit_work_form():
    """Formulario para editar trabajo existente"""
    st.subheader("✏️ Editar Trabajo Existente")
    st.info("Funcionalidad de edición de trabajos pendiente de implementar")

if __name__ == "__main__":
    main()
