from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database import Base

class Session(Base):
    """Modelo para las sesiones de chat"""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    context = Column(JSON, default=dict)
    completion_status = Column(JSON, default=dict)
    validation_state = Column(JSON, default=dict)
    agent_triggers = Column(JSON, default=dict)

    # Relación con mensajes
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    """Modelo para los mensajes del chat"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    text = Column(String, nullable=False)
    sender = Column(String, nullable=False)  # "user" o "bot"
    timestamp = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default=dict)

    # Relación con sesión
    session = relationship("Session", back_populates="messages") 