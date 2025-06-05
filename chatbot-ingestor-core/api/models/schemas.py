from typing import Dict, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel

class UserSessionCreate(BaseModel):
    """Modelo para crear una nueva sesión"""
    user_role: Literal["admin", "user", "analyst"]
    initial_data: Optional[Dict] = None

class SessionResponse(BaseModel):
    """Respuesta de creación de sesión"""
    session_id: str
    user_role: str
    created_at: datetime

class SessionDetailResponse(BaseModel):
    """Detalles completos de una sesión"""
    session_id: str
    user_role: str
    created_at: datetime
    completion_status: Dict[str, float]
    data: Dict
    validation_state: Dict
    agent_triggers: Dict

class ChatMessage(BaseModel):
    """Modelo para mensajes del chat"""
    text: str
    timestamp: datetime
    metadata: Optional[Dict] = None

class WebSocketMessage(BaseModel):
    """Modelo para mensajes WebSocket"""
    type: Literal["message", "status", "error"]
    data: Dict
    timestamp: datetime = datetime.utcnow() 