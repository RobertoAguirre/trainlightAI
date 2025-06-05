from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import time
from pydantic import BaseModel

class AgentResult(BaseModel):
    """Modelo para resultados de agentes"""
    success: bool
    data: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time: float
    metadata: Dict[str, Any] = {}

class BaseMarketAgent(ABC):
    """Clase base para todos los agentes de Market Analyzer"""
    
    def __init__(self, name: str, ai_client, config: Dict[str, Any]):
        self.name = name
        self.ai_client = ai_client
        self.config = config
        self.core_connector = None  # Se inicializará después
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Método principal - debe ser implementado por cada agente"""
        pass
    
    async def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validar que el contexto tenga los datos necesarios"""
        required_fields = self.config.get("required_fields", [])
        data = context.get("data", {})
        return all(field in data and data[field] for field in required_fields)
    
    async def register_with_core(self, core_url: str = "http://localhost:8000"):
        """Registrar agente con chatbot-ingestor-core"""
        if not self.core_connector:
            from integrations.core_connector import CoreConnector
            self.core_connector = CoreConnector(core_url)
        
        trigger_condition = self.config.get("trigger_condition")
        endpoint = f"{core_url}/agents/{self.name}/execute"
        
        await self.core_connector.register_agent(
            agent_name=self.name,
            trigger_condition=trigger_condition,
            endpoint=endpoint
        )
    
    async def update_context_results(self, session_id: str, results: Dict[str, Any]):
        """Actualizar contexto en el core con resultados del agente"""
        if not self.core_connector:
            raise RuntimeError("CoreConnector no inicializado")
            
        await self.core_connector.update_agent_results(
            session_id=session_id,
            agent_name=self.name,
            results=results
        )
    
    def _calculate_execution_time(self, start_time: float) -> float:
        """Calcular tiempo de ejecución"""
        return time.time() - start_time 