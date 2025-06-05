"""Agente para análisis secundario de mercado"""
from typing import Dict, Any
from datetime import datetime
import time
import json

from agents.base_agent import BaseMarketAgent, AgentResult
from integrations.anthropic_client import AnthropicClient
from .prompts import (
    VALIDATION_PROMPT,
    SWOT_PROMPT,
    FINANCIAL_PROMPT,
    STRATEGIC_PROMPT
)

class SecondaryAnalysisAgent(BaseMarketAgent):
    """Agente para análisis secundario profundo"""
    
    def __init__(self, config: Dict[str, Any]):
        # Configuración del cliente AI
        ai_client = AnthropicClient(config.get("anthropic_api_key"))
        super().__init__("secondary_analysis", ai_client, config)
    
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Análisis secundario basado en resultados del análisis primario
        
        Parámetros configurables en configs/agent_configs.py:
        - model: Modelo de Anthropic a utilizar
        - max_tokens: Máximo de tokens por respuesta
        - temperature: Temperatura para generación (0.1-1.0)
        """
        start_time = time.time()
        
        try:
            # Verificar análisis primario
            primary_results = self._get_primary_results(context)
            if not primary_results:
                return AgentResult(
                    success=False,
                    data={},
                    error_message="Se requiere análisis primario completado",
                    execution_time=self._calculate_execution_time(start_time)
                )
            
            company_data = context["data"]
            
            # Validación de datos primarios
            validation = await self._validate_primary_data(primary_results, company_data)
            
            # Análisis SWOT
            swot_analysis = await self._swot_analysis(company_data, primary_results)
            
            # Proyecciones financieras
            financial_projections = await self._financial_projections(primary_results)
            
            # Recomendaciones estratégicas
            strategic_recommendations = await self._strategic_recommendations(
                company_data,
                {
                    "primary": primary_results,
                    "swot": swot_analysis,
                    "financial": financial_projections
                }
            )
            
            results = {
                "validation": validation,
                "swot_analysis": swot_analysis,
                "financial_projections": financial_projections,
                "strategic_recommendations": strategic_recommendations,
                "confidence_score": self._calculate_confidence_score(validation),
                "analysis_date": datetime.now().isoformat()
            }
            
            return AgentResult(
                success=True,
                data=results,
                execution_time=self._calculate_execution_time(start_time),
                metadata={"model_used": self.config.get("model", "claude-3-sonnet-20240229")}
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                error_message=str(e),
                execution_time=self._calculate_execution_time(start_time)
            )
    
    def _get_primary_results(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener resultados del análisis primario"""
        return context.get("agent_triggers", {}).get("primary_analysis", {}).get("result", {})
    
    async def _validate_primary_data(
        self, 
        primary_results: Dict[str, Any], 
        company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validar y contrastar datos del análisis primario"""
        prompt = VALIDATION_PROMPT.format(
            company_data=json.dumps(company_data, indent=2),
            primary_results=json.dumps(primary_results, indent=2)
        )
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context={"primary": primary_results, "company": company_data},
            model=self.config.get("model", "claude-3-sonnet-20240229")
        )
        
        return json.loads(response)
    
    async def _swot_analysis(
        self, 
        company_data: Dict[str, Any], 
        market_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Análisis SWOT completo"""
        prompt = SWOT_PROMPT.format(
            company_data=json.dumps(company_data, indent=2),
            market_analysis=json.dumps(market_analysis, indent=2)
        )
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context={"company": company_data, "market": market_analysis},
            model=self.config.get("model", "claude-3-sonnet-20240229")
        )
        
        return json.loads(response)
    
    async def _financial_projections(self, market_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generar proyecciones financieras"""
        prompt = FINANCIAL_PROMPT.format(
            market_analysis=json.dumps(market_analysis, indent=2)
        )
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context={"market": market_analysis},
            model=self.config.get("model", "claude-3-sonnet-20240229")
        )
        
        return json.loads(response)
    
    async def _strategic_recommendations(
        self, 
        company_data: Dict[str, Any],
        previous_analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Desarrollar recomendaciones estratégicas"""
        prompt = STRATEGIC_PROMPT.format(
            company_data=json.dumps(company_data, indent=2),
            previous_analyses=json.dumps(previous_analyses, indent=2)
        )
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context={"company": company_data, "analyses": previous_analyses},
            model=self.config.get("model", "claude-3-sonnet-20240229")
        )
        
        return json.loads(response)
    
    def _calculate_confidence_score(self, validation: Dict[str, Any]) -> float:
        """Calcular score de confianza basado en validación"""
        # Implementación simple - puede ser más sofisticada
        confidence_factors = [
            validation.get("data_consistency", 0),
            validation.get("source_reliability", 0),
            validation.get("method_quality", 0)
        ]
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0 