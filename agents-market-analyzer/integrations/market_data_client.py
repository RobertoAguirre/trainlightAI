"""Cliente para fuentes de datos de mercado"""
from typing import Dict, Any, List, Optional
import aiohttp
from datetime import datetime

from utils.exceptions import DataSourceError
from utils.logger import AppLogger

class MarketDataClient:
    """Cliente para acceder a fuentes de datos de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el cliente"""
        self.config = config
        self.logger = AppLogger(__name__)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_market_data(self, market_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Obtiene datos de mercado"""
        try:
            if not self.session:
                raise DataSourceError("Cliente no inicializado")
            
            params = {
                "market_id": market_id,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            
            async with self.session.get(
                f"{self.config['api_url']}/market-data",
                params=params,
                headers=self.config.get("headers", {})
            ) as response:
                if response.status != 200:
                    raise DataSourceError(f"Error al obtener datos: {response.status}")
                
                return await response.json()
                
        except Exception as e:
            self.logger.error(f"Error al obtener datos de mercado: {str(e)}")
            raise DataSourceError(f"Error al obtener datos de mercado: {str(e)}")
    
    async def get_market_metrics(self, market_id: str) -> Dict[str, Any]:
        """Obtiene métricas de mercado"""
        try:
            if not self.session:
                raise DataSourceError("Cliente no inicializado")
            
            async with self.session.get(
                f"{self.config['api_url']}/market-metrics/{market_id}",
                headers=self.config.get("headers", {})
            ) as response:
                if response.status != 200:
                    raise DataSourceError(f"Error al obtener métricas: {response.status}")
                
                return await response.json()
                
        except Exception as e:
            self.logger.error(f"Error al obtener métricas de mercado: {str(e)}")
            raise DataSourceError(f"Error al obtener métricas de mercado: {str(e)}") 