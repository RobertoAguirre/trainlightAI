from typing import Any, Dict, Optional
from datetime import datetime
import json
import uuid
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.models.db_models import Session as DBSession, Message as DBMessage

class ContextData(BaseModel):
    """Modelo para los datos del contexto"""
    session_id: str
    user_role: str
    created_at: datetime
    data: Dict[str, Any]
    validation_state: Dict[str, Any]
    agent_triggers: Dict[str, Any]

class ContextManager:
    """Gestiona el contexto JSON por sesión con persistencia"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_session(self, user_role: str) -> str:
        """Crear nueva sesión con contexto inicial"""
        session = DBSession(
            user_role=user_role,
            context={},
            completion_status={},
            validation_state={},
            agent_triggers={}
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session.id
    
    async def update_context(self, session_id: str, field: str, value: Any) -> Dict[str, Any]:
        """Actualizar campo específico del contexto"""
        session = await self._get_session(session_id)
        if not session:
            raise ValueError(f"Sesión no encontrada: {session_id}")
        
        context = session.context or {}
        context[field] = value
        session.context = context
        
        await self.db.commit()
        await self.db.refresh(session)
        return context
    
    async def get_context(self, session_id: str) -> Dict[str, Any]:
        """Obtener contexto completo de sesión"""
        session = await self._get_session(session_id)
        if not session:
            raise ValueError(f"Sesión no encontrada: {session_id}")
        
        return {
            "session_id": session.id,
            "user_role": session.user_role,
            "created_at": session.created_at,
            "data": session.context or {},
            "validation_state": session.validation_state or {},
            "agent_triggers": session.agent_triggers or {}
        }
    
    async def get_completion_status(self, session_id: str) -> Dict[str, float]:
        """Calcular % completitud por categorías"""
        session = await self._get_session(session_id)
        if not session:
            raise ValueError(f"Sesión no encontrada: {session_id}")
        
        completion = session.completion_status or {}
        
        # Si no hay estado de completitud, calcularlo
        if not completion:
            context = session.context or {}
            total_fields = len(context)
            if total_fields > 0:
                filled_fields = sum(1 for v in context.values() if v is not None)
                completion["general"] = filled_fields / total_fields
                session.completion_status = completion
                await self.db.commit()
        
        return completion
    
    async def _get_session(self, session_id: str) -> Optional[DBSession]:
        """Obtener sesión de la base de datos"""
        result = await self.db.execute(
            select(DBSession)
            .options(selectinload(DBSession.messages))
            .where(DBSession.id == session_id)
        )
        return result.scalar_one_or_none() 