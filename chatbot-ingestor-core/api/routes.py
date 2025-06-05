from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from datetime import datetime
from typing import Dict, List

from .models.schemas import (
    UserSessionCreate,
    SessionResponse,
    SessionDetailResponse,
    ChatMessage,
    WebSocketMessage
)
from .dependencies import (
    ContextManagerDep,
    ValidationEngineDep,
    AgentOrchestratorDep,
    ChatbotIngestorDep
)

router = APIRouter()

# Almacén de conexiones WebSocket activas
active_connections: Dict[str, WebSocket] = {}

@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    user_data: UserSessionCreate,
    context_manager: ContextManagerDep
) -> SessionResponse:
    """Crear nueva sesión conversacional"""
    session_id = await context_manager.create_session(user_data.user_role)
    context = await context_manager.get_context(session_id)
    
    return SessionResponse(
        session_id=session_id,
        user_role=user_data.user_role,
        created_at=context["created_at"]
    )

@router.get("/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    context_manager: ContextManagerDep
) -> SessionDetailResponse:
    """Obtener estado completo de sesión"""
    try:
        context = await context_manager.get_context(session_id)
        completion = await context_manager.get_completion_status(session_id)
        
        return SessionDetailResponse(
            session_id=session_id,
            user_role=context["user_role"],
            created_at=context["created_at"],
            completion_status=completion,
            data=context["data"],
            validation_state=context["validation_state"],
            agent_triggers=context["agent_triggers"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.websocket("/chat/{session_id}")
async def chat_websocket(
    websocket: WebSocket,
    session_id: str,
    context_manager: ContextManagerDep,
    chatbot_ingestor: ChatbotIngestorDep
):
    """Chat en tiempo real - bidireccional"""
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_json()
            message = ChatMessage(**data)
            
            # Procesar mensaje con el ingestor
            result = await chatbot_ingestor.process_message(
                message.text,
                session_id,
                "user"  # TODO: Obtener rol real del contexto
            )
            
            # Enviar respuesta al cliente
            await websocket.send_json(WebSocketMessage(
                type="message",
                data={
                    "response": result.response_text,
                    "context": result.context_updated,
                    "validation": result.validation_status,
                    "agents": result.agents_triggered,
                    "next_action": result.next_suggested_action
                }
            ).dict())
            
    except WebSocketDisconnect:
        active_connections.pop(session_id, None)
    except Exception as e:
        await websocket.send_json(WebSocketMessage(
            type="error",
            data={"error": str(e)}
        ).dict())
        active_connections.pop(session_id, None) 