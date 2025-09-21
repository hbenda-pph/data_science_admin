"""
Conexión y operaciones con BigQuery para el sistema de administración
"""
import os
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from typing import List, Dict, Optional

class CategoriesDatabase:
    def __init__(self):
        """Inicializar conexión a BigQuery para categorías"""
        self.project_id = "platform-partners-des"
        self.dataset_id = "settings"
        self.table_id = "works_categories"
        self.table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        
        # Inicializar cliente BigQuery
        self.client = bigquery.Client(project=self.project_id)
    
    def get_all_categories(self) -> pd.DataFrame:
        """Obtener todas las categorías activas"""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE is_active = true
        ORDER BY display_order, category_name
        """
        return self.client.query(query).to_dataframe()
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict]:
        """Obtener categoría por ID"""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE category_id = @category_id
        LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("category_id", "STRING", category_id)
            ]
        )
        result = self.client.query(query, job_config=job_config).to_dataframe()
        return result.to_dict('records')[0] if not result.empty else None
    
    def create_category(self, category_data: Dict) -> bool:
        """Crear nueva categoría"""
        try:
            from datetime import datetime
            
            current_time = datetime.now().isoformat()
            row_to_insert = {
                "category_id": category_data["category_id"],
                "category_name": category_data["category_name"],
                "category_icon": category_data.get("category_icon", "📊"),
                "display_order": category_data.get("display_order", 999),
                "is_active": True,
                "created_date": current_time,
                "updated_date": current_time
            }
            
            errors = self.client.insert_rows_json(self.table_ref, [row_to_insert])
            return len(errors) == 0
            
        except Exception as e:
            print(f"Error creating category: {e}")
            return False
    
    def update_category(self, category_id: str, update_data: Dict) -> bool:
        """Actualizar categoría existente"""
        try:
            set_clauses = []
            for key, value in update_data.items():
                if key != "category_id":
                    if isinstance(value, str):
                        set_clauses.append(f"{key} = '{value}'")
                    else:
                        set_clauses.append(f"{key} = {value}")
            
            if not set_clauses:
                return True
            
            query = f"""
            UPDATE `{self.table_ref}`
            SET {', '.join(set_clauses)}, updated_date = CURRENT_TIMESTAMP()
            WHERE category_id = '{category_id}'
            """
            
            job = self.client.query(query)
            job.result()
            return True
            
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
    
    def archive_category(self, category_id: str) -> bool:
        """Archivar categoría (soft delete)"""
        try:
            query = f"""
            UPDATE `{self.table_ref}`
            SET is_active = false, updated_date = CURRENT_TIMESTAMP()
            WHERE category_id = '{category_id}'
            """
            
            job = self.client.query(query)
            job.result()
            return True
            
        except Exception as e:
            print(f"Error archiving category: {e}")
            return False

class WorksDatabase:
    def __init__(self):
        """Inicializar conexión a BigQuery para trabajos"""
        self.project_id = "platform-partners-des"
        self.dataset_id = "settings"
        self.table_id = "works_index"
        self.table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        
        # Inicializar cliente BigQuery
        self.client = bigquery.Client(project=self.project_id)
    
    def get_all_works(self) -> pd.DataFrame:
        """Obtener todos los trabajos"""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        ORDER BY category, created_date DESC
        """
        return self.client.query(query).to_dataframe()
    
    def get_work_by_id(self, work_id: str) -> Optional[Dict]:
        """Obtener trabajo por ID"""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE work_id = @work_id
        LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("work_id", "STRING", work_id)
            ]
        )
        result = self.client.query(query, job_config=job_config).to_dataframe()
        return result.to_dict('records')[0] if not result.empty else None
    
    def create_work(self, work_data: Dict) -> bool:
        """Crear nuevo trabajo"""
        try:
            from datetime import datetime
            
            current_time = datetime.now().isoformat()
            row_to_insert = {
                "work_id": work_data["work_id"],
                "work_name": work_data["work_name"],
                "work_slug": work_data.get("work_slug", work_data["work_id"]),
                "category": work_data["category"],
                "subcategory": work_data.get("subcategory", ""),
                "status": work_data["status"],
                "version": work_data["version"],
                "is_latest": work_data.get("is_latest", True),
                "description": work_data.get("description", ""),
                "short_description": work_data.get("short_description", ""),
                "image_preview_url": work_data.get("image_preview_url", ""),
                "created_date": current_time,
                "updated_date": current_time,
                "activated_date": work_data.get("activated_date"),
                "archived_date": work_data.get("archived_date"),
                "streamlit_page": work_data["streamlit_page"],
                "config_json": work_data.get("config_json", "{}"),
                "notes": work_data.get("notes", ""),
                "tags": work_data.get("tags", [])
            }
            
            errors = self.client.insert_rows_json(self.table_ref, [row_to_insert])
            return len(errors) == 0
            
        except Exception as e:
            print(f"Error creating work: {e}")
            return False
    
    def update_work(self, work_id: str, update_data: Dict) -> bool:
        """Actualizar trabajo existente"""
        try:
            set_clauses = []
            for key, value in update_data.items():
                if key != "work_id":
                    if isinstance(value, str):
                        set_clauses.append(f"{key} = '{value}'")
                    elif isinstance(value, list):
                        tags_str = "', '".join(value)
                        set_clauses.append(f"{key} = ['{tags_str}']")
                    else:
                        set_clauses.append(f"{key} = {value}")
            
            if not set_clauses:
                return True
            
            query = f"""
            UPDATE `{self.table_ref}`
            SET {', '.join(set_clauses)}, updated_date = CURRENT_TIMESTAMP()
            WHERE work_id = '{work_id}'
            """
            
            job = self.client.query(query)
            job.result()
            return True
            
        except Exception as e:
            print(f"Error updating work: {e}")
            return False
    
    def archive_work(self, work_id: str) -> bool:
        """Archivar trabajo (soft delete)"""
        try:
            query = f"""
            UPDATE `{self.table_ref}`
            SET status = 'archived', 
                archived_date = CURRENT_TIMESTAMP(),
                updated_date = CURRENT_TIMESTAMP()
            WHERE work_id = '{work_id}'
            """
            
            job = self.client.query(query)
            job.result()
            return True
            
        except Exception as e:
            print(f"Error archiving work: {e}")
            return False
