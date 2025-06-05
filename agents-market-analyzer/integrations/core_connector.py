import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime

class CoreConnector:
    """Conector para comunicación con chatbot-ingestor-core"""
    
    def __init__(self, core_api_url: str = "http://localhost:8000"):
        self.core_api_url = core_api_url
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
    
    async def register_agent(self, agent_name: str, trigger_condition: Dict[str, Any], endpoint: str):
        """Registrar agente con el AgentOrchestrator del core"""
        if not self._session:
            self._session = aiohttp.ClientSession()
            
        async with self._session.post(
            f"{self.core_api_url}/agents/register",
            json={
                "name": agent_name,
                "trigger_condition": trigger_condition,
                "endpoint": endpoint
            }
        ) as response:
            return await response.json()
    
    async def get_context(self, session_id: str) -> Dict[str, Any]:
        """Obtener contexto actual de una sesión"""
        if not self._session:
            self._session = aiohttp.ClientSession()
            
        async with self._session.get(
            f"{self.core_api_url}/sessions/{session_id}"
        ) as response:
            return await response.json()
    
    async def update_agent_results(self, session_id: str, agent_name: str, results: Dict[str, Any]):
        """Actualizar contexto con resultados del agente"""
        if not self._session:
            self._session = aiohttp.ClientSession()
            
        async with self._session.patch(
            f"{self.core_api_url}/sessions/{session_id}/agent_results",
            json={
                "agent_name": agent_name,
                "results": results
            }
        ) as response:
            return await response.json()
    
    async def notify_completion(self, session_id: str, agent_name: str, status: str):
        """Notificar al core que el agente terminó"""
        if not self._session:
            self._session = aiohttp.ClientSession()
            
        async with self._session.post(
            f"{self.core_api_url}/sessions/{session_id}/agent_status",
            json={
                "agent_name": agent_name,
                "status": status,
                "completed_at": datetime.now().isoformat()
            }
        ) as response:
            return await response.json() 