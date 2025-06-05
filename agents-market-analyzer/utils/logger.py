"""Logger para la aplicación"""
import logging
import sys
from typing import Optional

class AppLogger:
    """Logger personalizado para la aplicación"""
    
    def __init__(self, name: str, level: int = logging.INFO):
        """Inicializa el logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Configura los handlers del logger"""
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs) -> None:
        """Log nivel info"""
        self.logger.info(message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log nivel error"""
        self.logger.error(message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log nivel warning"""
        self.logger.warning(message, **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log nivel debug"""
        self.logger.debug(message, **kwargs) 