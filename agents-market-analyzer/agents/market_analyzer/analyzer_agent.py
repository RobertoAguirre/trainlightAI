"""Agente analizador de mercado"""
from typing import Dict, Any
import json
from datetime import datetime

from agents.base_agent import BaseMarketAgent
from agents.market_analyzer.prompts import ANALYSIS_PROMPT, VALIDATION_PROMPT

class MarketAnalyzerAgent(BaseMarketAgent):
    """Agente para analizar mercados"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente analizador"""
        super().__init__(config)
        self.analysis_config = {
            "min_completeness": config.get("min_completeness", 0.8),
            "min_accuracy": config.get("min_accuracy", 0.8),
            "min_relevance": config.get("min_relevance", 0.8)
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta el análisis de mercado"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Analizar mercado
            analysis = await self._analyze_market(context)
            
            # Validar resultados
            validation = await self._validate_results(analysis, context)
            
            # Aplicar ajustes si es necesario
            if not self._is_analysis_valid(validation):
                analysis = await self._apply_adjustments(analysis, validation)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "analysis": analysis,
                    "validation": validation,
                    "metadata": {
                        "analysis_time": datetime.now().isoformat(),
                        "config": self.analysis_config
                    }
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error_message": str(e)
            }
    
    def _validate_context(self, context: Dict[str, Any]) -> None:
        """Valida el contexto de entrada"""
        required_fields = ["company_name", "product_description", "target_market"]
        for field in required_fields:
            if field not in context.get("data", {}):
                raise ValueError(f"Falta el campo requerido: {field}")
    
    async def _analyze_market(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza el mercado objetivo"""
        prompt = ANALYSIS_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            market_data=json.dumps(context.get("market_data", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _validate_results(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Valida los resultados del análisis"""
        prompt = VALIDATION_PROMPT.format(
            analysis_results=json.dumps(analysis),
            validation_context=json.dumps(context)
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _is_analysis_valid(self, validation: Dict[str, Any]) -> bool:
        """Verifica si el análisis cumple con los criterios mínimos"""
        metrics = validation["validacion"]
        return (
            metrics["completitud"] >= self.analysis_config["min_completeness"] and
            metrics["precision"] >= self.analysis_config["min_accuracy"] and
            metrics["relevancia"] >= self.analysis_config["min_relevance"]
        )
    
    async def _apply_adjustments(self, analysis: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica ajustes sugeridos al análisis"""
        # Implementar lógica de ajustes basada en sugerencias
        return analysis 