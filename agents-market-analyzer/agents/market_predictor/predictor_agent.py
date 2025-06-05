"""Agente para predicción de mercado"""
from typing import Dict, Any, List
import time
import json
from datetime import datetime, timedelta
import numpy as np
from scipy import stats

from agents.base_agent import BaseMarketAgent, AgentResult
from integrations.openai_client import OpenAIClient
from .prompts import (
    MARKET_PREDICTION_PROMPT,
    TREND_ANALYSIS_PROMPT,
    RISK_ASSESSMENT_PROMPT,
    SCENARIO_PLANNING_PROMPT,
    PREDICTION_PROMPT,
    VALIDATION_PROMPT
)

class MarketPredictorAgent(BaseMarketAgent):
    """Agente para predecir tendencias de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente predictor"""
        super().__init__(config)
        self.prediction_config = {
            "min_confidence": config.get("min_confidence", 0.8),
            "min_consistency": config.get("min_consistency", 0.8),
            "min_foundation": config.get("min_foundation", 0.8)
        }
        
        # Configuración del cliente AI
        ai_client = OpenAIClient(config.get("openai_api_key"))
        super().__init__("market_predictor", ai_client, config)
        
        # Configuración de predicción
        self.time_horizon = config.get("time_horizon", 12)  # meses
        self.confidence_level = config.get("confidence_level", 95)  # porcentaje
        self.detail_level = config.get("detail_level", "high")
        
        # Inicializar modelos
        self._init_models()
    
    def _init_models(self):
        """Inicializar modelos de predicción"""
        self.trend_model = None
        self.risk_model = None
        self.scenario_model = None
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la predicción de mercado"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Generar predicciones
            predictions = await self._generate_predictions(context)
            
            # Validar resultados
            validation = await self._validate_predictions(predictions, context)
            
            # Aplicar ajustes si es necesario
            if not self._are_predictions_valid(validation):
                predictions = await self._apply_adjustments(predictions, validation)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "predictions": predictions,
                    "validation": validation,
                    "metadata": {
                        "prediction_time": datetime.now().isoformat(),
                        "config": self.prediction_config
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
    
    async def _generate_predictions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Genera predicciones de mercado"""
        prompt = PREDICTION_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            market_analysis=json.dumps(context.get("market_analysis", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _validate_predictions(self, predictions: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Valida las predicciones generadas"""
        prompt = VALIDATION_PROMPT.format(
            predictions=json.dumps(predictions),
            validation_context=json.dumps(context)
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _are_predictions_valid(self, validation: Dict[str, Any]) -> bool:
        """Verifica si las predicciones cumplen con los criterios mínimos"""
        metrics = validation["validacion"]
        return (
            metrics["confiabilidad"] >= self.prediction_config["min_confidence"] and
            metrics["consistencia"] >= self.prediction_config["min_consistency"] and
            metrics["fundamentacion"] >= self.prediction_config["min_foundation"]
        )
    
    async def _apply_adjustments(self, predictions: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica ajustes sugeridos a las predicciones"""
        # Implementar lógica de ajustes basada en sugerencias
        return predictions
    
    async def _analyze_trends(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar tendencias de mercado"""
        prompt = TREND_ANALYSIS_PROMPT.format(
            industry=context["data"].get("industry", "N/A"),
            time_period=f"{self.time_horizon} meses"
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _assess_risks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluar riesgos de mercado"""
        prompt = RISK_ASSESSMENT_PROMPT.format(
            company_name=context["data"]["company_name"],
            target_market=context["data"]["target_market"],
            detail_level=self.detail_level
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _generate_scenarios(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generar escenarios de mercado"""
        prompt = SCENARIO_PLANNING_PROMPT.format(
            product_description=context["data"]["product_description"],
            time_horizon=f"{self.time_horizon} meses"
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    def _calculate_confidence_metrics(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular métricas de confianza para las predicciones"""
        metrics = {}
        
        # Calcular intervalos de confianza
        for key, value in predictions.items():
            if isinstance(value, (int, float)):
                # Calcular intervalo de confianza
                confidence_interval = stats.norm.interval(
                    self.confidence_level / 100,
                    loc=value,
                    scale=value * 0.1  # Asumir desviación estándar del 10%
                )
                metrics[key] = {
                    "value": value,
                    "confidence_interval": confidence_interval,
                    "confidence_level": self.confidence_level
                }
        
        return metrics
    
    def _calculate_prediction_quality(self, results: Dict[str, Any]) -> float:
        """Calcular calidad de las predicciones"""
        # Factores de calidad
        factors = {
            "trend_consistency": self._calculate_trend_consistency(results["trend_analysis"]),
            "risk_coverage": self._calculate_risk_coverage(results["risk_assessment"]),
            "scenario_balance": self._calculate_scenario_balance(results["scenarios"]),
            "confidence_level": self.confidence_level / 100
        }
        
        # Calcular score final
        weights = {
            "trend_consistency": 0.3,
            "risk_coverage": 0.3,
            "scenario_balance": 0.2,
            "confidence_level": 0.2
        }
        
        quality_score = sum(
            factors[key] * weights[key]
            for key in factors
        )
        
        return quality_score
    
    def _calculate_trend_consistency(self, trend_analysis: Dict[str, Any]) -> float:
        """Calcular consistencia de tendencias"""
        # Implementar lógica de consistencia
        return 0.8  # Valor de ejemplo
    
    def _calculate_risk_coverage(self, risk_assessment: Dict[str, Any]) -> float:
        """Calcular cobertura de riesgos"""
        # Implementar lógica de cobertura
        return 0.9  # Valor de ejemplo
    
    def _calculate_scenario_balance(self, scenarios: Dict[str, Any]) -> float:
        """Calcular balance de escenarios"""
        # Implementar lógica de balance
        return 0.85  # Valor de ejemplo 