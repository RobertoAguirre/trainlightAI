"""Agente para recopilación y análisis de datos de mercado"""
from typing import Dict, Any
import time
import json
from datetime import datetime

from agents.base_agent import BaseMarketAgent, AgentResult
from integrations.openai_client import OpenAIClient
from .prompts import (
    MARKET_DATA_PROMPT,
    INDUSTRY_METRICS_PROMPT,
    CONSUMER_BEHAVIOR_PROMPT,
    COMPETITIVE_LANDSCAPE_PROMPT
)

class MarketDataAgent(BaseMarketAgent):
    """Agente para recopilación y análisis de datos de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        # Configuración del cliente AI
        ai_client = OpenAIClient(config.get("openai_api_key"))
        super().__init__("market_data", ai_client, config)
    
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Ejecuta el análisis de datos de mercado
        
        Parámetros configurables en configs/agent_configs.py:
        - model: Modelo de OpenAI a utilizar
        - max_tokens: Máximo de tokens por respuesta
        - temperature: Temperatura para generación (0.1-1.0)
        """
        start_time = time.time()
        
        try:
            # Validar contexto
            if not self._validate_context(context):
                return AgentResult(
                    success=False,
                    data={},
                    error_message="Contexto inválido: faltan datos requeridos",
                    execution_time=self._calculate_execution_time(start_time)
                )
            
            # Recopilar datos del mercado
            market_data = await self._collect_market_data(context)
            
            # Analizar métricas de la industria
            industry_metrics = await self._analyze_industry_metrics(context)
            
            # Analizar comportamiento del consumidor
            consumer_behavior = await self._analyze_consumer_behavior(context)
            
            # Analizar panorama competitivo
            competitive_landscape = await self._analyze_competitive_landscape(context)
            
            # Compilar resultados
            results = {
                "market_data": market_data,
                "industry_metrics": industry_metrics,
                "consumer_behavior": consumer_behavior,
                "competitive_landscape": competitive_landscape,
                "timestamp": datetime.now().isoformat()
            }
            
            return AgentResult(
                success=True,
                data=results,
                execution_time=self._calculate_execution_time(start_time),
                metadata={
                    "model_used": self.config.get("model", "gpt-4"),
                    "data_points": len(results)
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                error_message=str(e),
                execution_time=self._calculate_execution_time(start_time)
            )
    
    def _validate_context(self, context: Dict[str, Any]) -> bool:
        """Validar que el contexto contiene los datos necesarios"""
        required_fields = ["company_name", "product_description", "target_market"]
        return all(field in context.get("data", {}) for field in required_fields)
    
    async def _collect_market_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recopilar datos generales del mercado"""
        prompt = MARKET_DATA_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"]
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _analyze_industry_metrics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar métricas específicas de la industria"""
        prompt = INDUSTRY_METRICS_PROMPT.format(
            industry=context["data"].get("industry", "N/A"),
            region=context["data"].get("region", "N/A")
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _analyze_consumer_behavior(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar comportamiento del consumidor"""
        prompt = CONSUMER_BEHAVIOR_PROMPT.format(
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"]
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _analyze_competitive_landscape(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar panorama competitivo"""
        prompt = COMPETITIVE_LANDSCAPE_PROMPT.format(
            company_name=context["data"]["company_name"],
            industry=context["data"].get("industry", "N/A")
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response) 