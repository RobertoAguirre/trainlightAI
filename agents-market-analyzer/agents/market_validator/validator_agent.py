"""Agente validador de mercado"""
from typing import Dict, Any
import json
from datetime import datetime

from agents.base_agent import BaseMarketAgent
from agents.market_validator.prompts import VALIDATION_PROMPT, CORRECTION_PROMPT
from utils.ai_client import OpenAIClient

class MarketValidatorAgent(BaseMarketAgent):
    """Agente para validar análisis de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente validador"""
        super().__init__(config)
        self.ai_client = OpenAIClient(
            api_key=config["openai_api_key"],
            model=config.get("model", "gpt-4"),
            max_tokens=config.get("max_tokens", 2000),
            temperature=config.get("temperature", 0.7)
        )
        self.validation_config = {
            "min_completeness": config.get("min_completeness", 0.8),
            "min_consistency": config.get("min_consistency", 0.8),
            "min_reliability": config.get("min_reliability", 0.8)
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la validación del análisis"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Validar resultados
            validation = await self._validate_results(context)
            
            # Aplicar correcciones si es necesario
            if not self._is_validation_valid(validation):
                corrections = await self._generate_corrections(validation, context)
                corrected_results = await self._apply_corrections(context, corrections)
            else:
                corrections = None
                corrected_results = context.get("analysis_results", {})
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "validation": validation,
                    "corrections": corrections,
                    "corrected_results": corrected_results,
                    "metadata": {
                        "validation_time": datetime.now().isoformat(),
                        "config": self.validation_config
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
    
    async def _validate_results(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Valida los resultados del análisis"""
        prompt = VALIDATION_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            analysis_results=json.dumps(context.get("analysis_results", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _is_validation_valid(self, validation: Dict[str, Any]) -> bool:
        """Verifica si la validación cumple con los criterios mínimos"""
        metrics = validation["validacion"]
        return (
            metrics["completitud"] >= self.validation_config["min_completeness"] and
            metrics["consistencia"] >= self.validation_config["min_consistency"] and
            metrics["confiabilidad"] >= self.validation_config["min_reliability"]
        )
    
    async def _generate_corrections(self, validation: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Genera correcciones para los errores encontrados"""
        prompt = CORRECTION_PROMPT.format(
            validation_results=json.dumps(validation),
            context=json.dumps(context)
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _apply_corrections(self, context: Dict[str, Any], corrections: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica las correcciones generadas"""
        # Implementar lógica de aplicación de correcciones
        return context.get("analysis_results", {}) 