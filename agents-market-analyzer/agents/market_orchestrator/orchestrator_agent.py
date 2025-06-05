"""Agente orquestador de mercado"""
from typing import Dict, Any, List
import json
from datetime import datetime

from agents.base_agent import BaseMarketAgent
from agents.market_orchestrator.prompts import ORCHESTRATION_PROMPT, VALIDATION_PROMPT

class MarketOrchestratorAgent(BaseMarketAgent):
    """Agente para orquestar el flujo de análisis de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente orquestador"""
        super().__init__(config)
        self.orchestration_config = {
            "max_retries": config.get("max_retries", 3),
            "timeout": config.get("timeout", 300),
            "parallel_execution": config.get("parallel_execution", True)
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la orquestación del análisis"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Generar plan de ejecución
            execution_plan = await self._generate_execution_plan(context)
            
            # Validar plan
            validation = await self._validate_plan(execution_plan, context)
            
            # Ajustar plan si es necesario
            if not self._is_plan_valid(validation):
                execution_plan = await self._adjust_plan(execution_plan, validation)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "execution_plan": execution_plan,
                    "validation": validation,
                    "metadata": {
                        "orchestration_time": datetime.now().isoformat(),
                        "config": self.orchestration_config
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
    
    async def _generate_execution_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Genera el plan de ejecución"""
        prompt = ORCHESTRATION_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            analysis_requirements=json.dumps(context.get("analysis_requirements", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _validate_plan(self, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Valida el plan de ejecución"""
        prompt = VALIDATION_PROMPT.format(
            orchestration_plan=json.dumps(plan),
            validation_context=json.dumps(context)
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _is_plan_valid(self, validation: Dict[str, Any]) -> bool:
        """Verifica si el plan es válido"""
        metrics = validation["validacion"]
        return (
            metrics["completitud"] >= 0.8 and
            metrics["coherencia"] >= 0.8 and
            metrics["viabilidad"] >= 0.8
        )
    
    async def _adjust_plan(self, plan: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """Ajusta el plan basado en la validación"""
        # Implementar lógica de ajustes basada en sugerencias
        return plan 