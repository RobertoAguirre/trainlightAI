"""Agente integrador de mercado"""
from typing import Dict, Any
import json
from datetime import datetime

from agents.base_agent import BaseMarketAgent
from agents.market_integrator.prompts import INTEGRATION_PROMPT, CONSISTENCY_CHECK_PROMPT
from utils.ai_client import OpenAIClient

class MarketIntegratorAgent(BaseMarketAgent):
    """Agente para integrar resultados de análisis de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente integrador"""
        super().__init__(config)
        self.ai_client = OpenAIClient(
            api_key=config["openai_api_key"],
            model=config.get("model", "gpt-4"),
            max_tokens=config.get("max_tokens", 2000),
            temperature=config.get("temperature", 0.7)
        )
        self.integration_config = {
            "min_consistency": config.get("min_consistency", 0.8),
            "min_coherence": config.get("min_coherence", 0.8),
            "min_reliability": config.get("min_reliability", 0.8)
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la integración de resultados"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Integrar resultados
            integrated_results = await self._integrate_results(context)
            
            # Verificar consistencia
            consistency_check = await self._check_consistency(integrated_results, context)
            
            # Aplicar ajustes si es necesario
            if not self._are_results_consistent(consistency_check):
                integrated_results = await self._apply_adjustments(integrated_results, consistency_check)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "integrated_results": integrated_results,
                    "consistency_check": consistency_check,
                    "metadata": {
                        "integration_time": datetime.now().isoformat(),
                        "config": self.integration_config
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
    
    async def _integrate_results(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Integra los resultados de análisis"""
        prompt = INTEGRATION_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            analysis_results=json.dumps(context.get("analysis_results", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _check_consistency(self, results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica la consistencia de los resultados integrados"""
        prompt = CONSISTENCY_CHECK_PROMPT.format(
            integrated_results=json.dumps(results),
            validation_context=json.dumps(context)
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _are_results_consistent(self, consistency_check: Dict[str, Any]) -> bool:
        """Verifica si los resultados cumplen con los criterios mínimos"""
        metrics = consistency_check["validacion"]
        return (
            metrics["consistencia"] >= self.integration_config["min_consistency"] and
            metrics["coherencia"] >= self.integration_config["min_coherence"] and
            metrics["confiabilidad"] >= self.integration_config["min_reliability"]
        )
    
    async def _apply_adjustments(self, results: Dict[str, Any], consistency_check: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica ajustes sugeridos a los resultados"""
        # Implementar lógica de ajustes basada en sugerencias
        return results 