from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

from .context import ContextManager
from .validation import ValidationEngine, ValidationResult
from .orchestrator import AgentOrchestrator

class ProcessResult(BaseModel):
    """Resultado del procesamiento de un mensaje"""
    response_text: str
    context_updated: Dict[str, Any]
    validation_status: Dict[str, Any]
    agents_triggered: List[str]
    next_suggested_action: Optional[str]

class ChatbotIngestor:
    """Motor principal - integra todos los componentes"""
    
    def __init__(self, context_manager: ContextManager, validation_engine: ValidationEngine, agent_orchestrator: AgentOrchestrator):
        self.context = context_manager
        self.validation = validation_engine
        self.orchestrator = agent_orchestrator
    
    async def process_message(self, text: str, session_id: str, user_role: str) -> ProcessResult:
        """Procesar mensaje del usuario - flujo principal"""
        # 1. Extraer intención/datos del mensaje
        intent, extracted_data = await self._extract_intent_and_data(text)
        
        # 2. Actualizar contexto
        context = await self.context.get_context(session_id)
        for field, value in extracted_data.items():
            await self.context.update_context(session_id, field, value)
        
        # 3. Validar nueva información
        validation_results = {}
        for field, value in extracted_data.items():
            validation_results[field] = await self.validation.validate_field(field, value, context)
        
        # 4. Verificar triggers de agentes
        triggered_agents = await self.orchestrator.check_triggers(context)
        agent_results = {}
        for agent_name in triggered_agents:
            agent_results[agent_name] = await self.orchestrator.invoke_agent(agent_name, context)
        
        # 5. Generar respuesta contextual
        next_action = await self.validation.suggest_next_action(context)
        
        return ProcessResult(
            response_text=self._generate_response(intent, validation_results, agent_results),
            context_updated=context,
            validation_status=validation_results,
            agents_triggered=triggered_agents,
            next_suggested_action=next_action
        )
    
    async def _extract_intent_and_data(self, text: str) -> tuple[str, Dict[str, Any]]:
        """Extraer intención y datos del mensaje del usuario"""
        # Implementación básica - se puede mejorar con NLP
        intent = "unknown"
        data = {}
        
        # Ejemplo simple de extracción
        if "empresa" in text.lower():
            intent = "company_info"
            data["company_type"] = "startup" if "startup" in text.lower() else "empresa"
        
        return intent, data
    
    def _generate_response(self, intent: str, validation_results: Dict[str, ValidationResult], agent_results: Dict[str, Any]) -> str:
        """Generar respuesta basada en el contexto actual"""
        # Implementación básica - se puede mejorar con templates o LLM
        if intent == "company_info":
            return "Gracias por la información sobre tu empresa. ¿Podrías contarme más sobre tu producto principal?"
        
        return "Entiendo. ¿Hay algo más que necesites compartir?" 