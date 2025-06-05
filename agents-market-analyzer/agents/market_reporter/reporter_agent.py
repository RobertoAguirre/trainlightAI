"""Agente reportero de mercado"""
from typing import Dict, Any
import json
from datetime import datetime

from agents.base_agent import BaseMarketAgent
from agents.market_reporter.prompts import REPORT_GENERATION_PROMPT, REPORT_VALIDATION_PROMPT
from utils.ai_client import OpenAIClient

class MarketReporterAgent(BaseMarketAgent):
    """Agente para generar reportes de análisis de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente reportero"""
        super().__init__(config)
        self.ai_client = OpenAIClient(
            api_key=config["openai_api_key"],
            model=config.get("model", "gpt-4"),
            max_tokens=config.get("max_tokens", 2000),
            temperature=config.get("temperature", 0.7)
        )
        self.report_config = {
            "min_completeness": config.get("min_completeness", 0.8),
            "min_clarity": config.get("min_clarity", 0.8),
            "min_accuracy": config.get("min_accuracy", 0.8)
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la generación del reporte"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Generar reporte
            report = await self._generate_report(context)
            
            # Validar reporte
            validation = await self._validate_report(report, context)
            
            # Aplicar ajustes si es necesario
            if not self._is_report_valid(validation):
                report = await self._apply_adjustments(report, validation)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "report": report,
                    "validation": validation,
                    "metadata": {
                        "generation_time": datetime.now().isoformat(),
                        "config": self.report_config
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
    
    async def _generate_report(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Genera el reporte de análisis"""
        prompt = REPORT_GENERATION_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            analysis_results=json.dumps(context.get("analysis_results", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _validate_report(self, report: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Valida el reporte generado"""
        prompt = REPORT_VALIDATION_PROMPT.format(
            report=json.dumps(report),
            context=json.dumps(context)
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _is_report_valid(self, validation: Dict[str, Any]) -> bool:
        """Verifica si el reporte cumple con los criterios mínimos"""
        metrics = validation["validacion"]
        return (
            metrics["completitud"] >= self.report_config["min_completeness"] and
            metrics["claridad"] >= self.report_config["min_clarity"] and
            metrics["precision"] >= self.report_config["min_accuracy"]
        )
    
    async def _apply_adjustments(self, report: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica ajustes sugeridos al reporte"""
        # Implementar lógica de ajustes basada en sugerencias
        return report 