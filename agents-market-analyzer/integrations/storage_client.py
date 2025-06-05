"""Cliente para almacenamiento de datos"""
from typing import Dict, Any, Optional, List
import json
import os
from datetime import datetime

from utils.exceptions import DataSourceError
from utils.logger import AppLogger

class StorageClient:
    """Cliente para almacenamiento de datos"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el cliente"""
        self.config = config
        self.logger = AppLogger(__name__)
        self.storage_path = config.get("storage_path", "data")
        
        # Crear directorio de almacenamiento si no existe
        os.makedirs(self.storage_path, exist_ok=True)
    
    async def save_data(self, data: Dict[str, Any], filename: str) -> str:
        """Guarda datos en archivo"""
        try:
            filepath = os.path.join(self.storage_path, filename)
            
            # Agregar metadata
            data_with_metadata = {
                "data": data,
                "metadata": {
                    "saved_at": datetime.now().isoformat(),
                    "version": self.config.get("version", "1.0")
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(data_with_metadata, f, indent=2)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error al guardar datos: {str(e)}")
            raise DataSourceError(f"Error al guardar datos: {str(e)}")
    
    async def load_data(self, filename: str) -> Dict[str, Any]:
        """Carga datos desde archivo"""
        try:
            filepath = os.path.join(self.storage_path, filename)
            
            if not os.path.exists(filepath):
                raise DataSourceError(f"Archivo no encontrado: {filename}")
            
            with open(filepath, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error al cargar datos: {str(e)}")
            raise DataSourceError(f"Error al cargar datos: {str(e)}")
    
    async def list_files(self, pattern: Optional[str] = None) -> List[str]:
        """Lista archivos en el directorio de almacenamiento"""
        try:
            files = os.listdir(self.storage_path)
            if pattern:
                files = [f for f in files if pattern in f]
            return files
            
        except Exception as e:
            self.logger.error(f"Error al listar archivos: {str(e)}")
            raise DataSourceError(f"Error al listar archivos: {str(e)}") 