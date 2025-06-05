from typing import Any, Callable, Dict, List, Optional
import aiohttp
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """Configuración de un agente"""
    name: str
    trigger_condition: Callable[[Dict[str, Any]], bool]
    endpoint: str

class AgentOrchestrator:
    """Disparador de agentes post-validación"""
    
    def __init__(self):
        self.registered_agents: Dict[str, AgentConfig] = {}
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def register_agent(self, name: str, trigger_condition: Callable[[Dict[str, Any]], bool], endpoint: str):
        """Registrar agente con condición de disparo"""
        self.registered_agents[name] = AgentConfig(
            name=name,
            trigger_condition=trigger_condition,
            endpoint=endpoint
        )
    
    async def check_triggers(self, context: Dict[str, Any]) -> List[str]:
        """Verificar qué agentes deben ejecutarse"""
        triggered_agents = []
        for name, config in self.registered_agents.items():
            if config.trigger_condition(context):
                triggered_agents.append(name)
        return triggered_agents
    
    async def invoke_agent(self, agent_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Invocar agente específico con contexto"""
        if agent_name not in self.registered_agents:
            raise ValueError(f"Agente no encontrado: {agent_name}")
        
        agent = self.registered_agents[agent_name]
        
        if self._session is None:
            self._session = aiohttp.ClientSession()
        
        try:
            async with self._session.post(agent.endpoint, json=context) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Error al invocar agente: {response.status}")
        except Exception as e:
            raise Exception(f"Error al comunicarse con el agente: {str(e)}")
    
    async def close(self):
        """Cerrar sesión HTTP"""
        if self._session:
            await self._session.close()
            self._session = None 