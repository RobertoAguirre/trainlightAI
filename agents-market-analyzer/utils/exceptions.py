"""Excepciones personalizadas para la aplicación"""

class MarketAnalysisError(Exception):
    """Error base para análisis de mercado"""
    pass

class ValidationError(MarketAnalysisError):
    """Error en validación de datos"""
    pass

class IntegrationError(MarketAnalysisError):
    """Error en integración de servicios"""
    pass

class ConfigurationError(MarketAnalysisError):
    """Error en configuración"""
    pass

class DataSourceError(MarketAnalysisError):
    """Error en fuente de datos"""
    pass

class AgentError(MarketAnalysisError):
    """Error en ejecución de agente"""
    pass 