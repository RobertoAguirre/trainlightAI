"""Configuración de logs de la aplicación"""
import logging
import os
from typing import Dict, Any

def setup_logging() -> Dict[str, Any]:
    """Configura el sistema de logs"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": log_format
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": log_level,
                "formatter": "standard",
                "filename": "app.log",
                "mode": "a"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True
            }
        }
    } 