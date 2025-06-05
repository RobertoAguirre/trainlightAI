"""Configuración general de la aplicación"""
from typing import Dict, Any
import os

def load_config() -> Dict[str, Any]:
    """Carga la configuración de la aplicación"""
    return {
        "app": {
            "name": "Market Analysis System",
            "version": "1.0.0",
            "environment": os.getenv("APP_ENV", "development")
        },
        "api": {
            "host": os.getenv("API_HOST", "0.0.0.0"),
            "port": int(os.getenv("API_PORT", "8000")),
            "debug": os.getenv("API_DEBUG", "true").lower() == "true"
        },
        "storage": {
            "path": os.getenv("STORAGE_PATH", "data"),
            "version": "1.0"
        },
        "market_data": {
            "api_url": os.getenv("MARKET_DATA_API_URL", "http://api.market-data.com"),
            "api_key": os.getenv("MARKET_DATA_API_KEY", ""),
            "timeout": int(os.getenv("MARKET_DATA_TIMEOUT", "30"))
        },
        "ai": {
            "provider": os.getenv("AI_PROVIDER", "openai"),
            "model": os.getenv("AI_MODEL", "gpt-4"),
            "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("AI_MAX_TOKENS", "2000"))
        }
    } 