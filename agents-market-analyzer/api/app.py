"""API para integración con chatbot-ingestor-core"""
from fastapi import FastAPI, WebSocket, HTTPException
from typing import Dict, Any
import json
import asyncio
from datetime import datetime

from configs.app_config import load_config
from agents.market_orchestrator.orchestrator_agent import MarketOrchestratorAgent

app = FastAPI(title="Market Analysis API")
config = load_config()
orchestrator = MarketOrchestratorAgent(config)

# Almacenamiento temporal de sesiones
sessions: Dict[str, Dict[str, Any]] = {}

@app.post("/sessions")
async def create_session():
    """Crear nueva sesión de análisis"""
    session_id = f"session_{datetime.now().timestamp()}"
    sessions[session_id] = {
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "context": {}
    }
    return {"session_id": session_id}

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Obtener estado de la sesión"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sessions[session_id]

@app.websocket("/chat/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Endpoint WebSocket para chat en tiempo real"""
    await websocket.accept()
    
    if session_id not in sessions:
        await websocket.close(code=4004, reason="Sesión no encontrada")
        return
    
    try:
        while True:
            # Recibir mensaje del core
            message = await websocket.receive_text()
            data = json.loads(message)
            
            # Actualizar contexto de la sesión
            sessions[session_id]["context"].update(data.get("context", {}))
            
            # Ejecutar análisis
            result = await orchestrator.execute(sessions[session_id]["context"])
            
            # Enviar resultado al core
            await websocket.send_json({
                "type": "analysis_result",
                "data": result
            })
            
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close() 