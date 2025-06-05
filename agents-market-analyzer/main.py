"""Aplicación principal de análisis de mercado"""
import asyncio
import logging
from typing import Dict, Any

from configs.app_config import load_config
from configs.logging_config import setup_logging
from utils.logger import AppLogger
from agents.market_analyzer.analyzer_agent import MarketAnalyzerAgent
from agents.market_predictor.predictor_agent import MarketPredictorAgent
from agents.market_visualizer.visualizer_agent import MarketVisualizerAgent
from agents.market_integrator.integrator_agent import MarketIntegratorAgent
from agents.market_orchestrator.orchestrator_agent import MarketOrchestratorAgent

async def main():
    """Función principal"""
    # Cargar configuración
    config = load_config()
    
    # Configurar logging
    logging_config = setup_logging()
    logging.config.dictConfig(logging_config)
    logger = AppLogger(__name__)
    
    try:
        # Inicializar agentes
        analyzer = MarketAnalyzerAgent(config)
        predictor = MarketPredictorAgent(config)
        visualizer = MarketVisualizerAgent(config)
        integrator = MarketIntegratorAgent(config)
        orchestrator = MarketOrchestratorAgent(config)
        
        # Ejecutar análisis
        context = {
            "data": {
                "company_name": "Empresa Ejemplo",
                "product_description": "Producto de ejemplo",
                "target_market": "Mercado objetivo"
            }
        }
        
        result = await orchestrator.execute(context)
        
        if result["success"]:
            logger.info("Análisis completado exitosamente")
        else:
            logger.error(f"Error en el análisis: {result.get('error_message')}")
            
    except Exception as e:
        logger.error(f"Error en la aplicación: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 