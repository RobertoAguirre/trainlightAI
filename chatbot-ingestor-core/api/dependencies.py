from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core import ContextManager, ValidationEngine, AgentOrchestrator, ChatbotIngestor
from .database import get_db

# Instancias singleton de los componentes core
_validation_engine = ValidationEngine()
_agent_orchestrator = AgentOrchestrator()

async def get_context_manager(db: AsyncSession = Depends(get_db)) -> ContextManager:
    """Dependency para obtener el ContextManager"""
    return ContextManager(db)

async def get_validation_engine() -> ValidationEngine:
    """Dependency para obtener el ValidationEngine"""
    return _validation_engine

async def get_agent_orchestrator() -> AgentOrchestrator:
    """Dependency para obtener el AgentOrchestrator"""
    return _agent_orchestrator

async def get_chatbot_ingestor(
    context_manager: ContextManager = Depends(get_context_manager),
    validation_engine: ValidationEngine = Depends(get_validation_engine),
    agent_orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator)
) -> ChatbotIngestor:
    """Dependency para obtener el ChatbotIngestor"""
    return ChatbotIngestor(context_manager, validation_engine, agent_orchestrator)

# Type aliases para las dependencias
ContextManagerDep = Annotated[ContextManager, Depends(get_context_manager)]
ValidationEngineDep = Annotated[ValidationEngine, Depends(get_validation_engine)]
AgentOrchestratorDep = Annotated[AgentOrchestrator, Depends(get_agent_orchestrator)]
ChatbotIngestorDep = Annotated[ChatbotIngestor, Depends(get_chatbot_ingestor)] 