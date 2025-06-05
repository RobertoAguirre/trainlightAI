"""Agente para análisis primario de mercado"""
from typing import Dict, Any, List
from datetime import datetime
import time
import json

from agents.base_agent import BaseMarketAgent, AgentResult
from integrations.openai_client import OpenAIClient
from .prompts import (
    MARKET_SIZE_PROMPT,
    COMPETITORS_PROMPT,
    TRENDS_PROMPT,
    OPPORTUNITIES_PROMPT
)

class PrimaryAnalysisAgent(BaseMarketAgent):
    """Agente para análisis primario de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        # Configuración del cliente AI
        ai_client = OpenAIClient(config.get("openai_api_key"))
        super().__init__("primary_analysis", ai_client, config)
    
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Realizar análisis primario basado en:
        - Información de la empresa
        - Descripción del producto
        - Mercado objetivo
        
        Parámetros configurables en configs/agent_configs.py:
        - model: Modelo de OpenAI a utilizar
        - max_tokens: Máximo de tokens por respuesta
        - temperature: Temperatura para generación (0.1-1.0)
        """
        start_time = time.time()
        
        try:
            if not await self.validate_context(context):
                return AgentResult(
                    success=False,
                    data={},
                    error_message="Datos insuficientes para análisis primario",
                    execution_time=self._calculate_execution_time(start_time)
                )
            
            company_data = context["data"]
            
            # Análisis del tamaño de mercado
            market_size = await self._analyze_market_size(company_data)
            
            # Identificación de competidores
            competitors = await self._identify_competitors(company_data)
            
            # Análisis de tendencias
            trends = await self._analyze_trends(company_data)
            
            # Identificación de oportunidades
            opportunities = await self._identify_opportunities(
                company_data, 
                market_size, 
                trends
            )
            
            results = {
                "market_size": market_size,
                "competitors": competitors,
                "trends": trends,
                "opportunities": opportunities,
                "analysis_date": datetime.now().isoformat()
            }
            
            return AgentResult(
                success=True,
                data=results,
                execution_time=self._calculate_execution_time(start_time),
                metadata={"model_used": self.config.get("model", "gpt-4")}
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                error_message=str(e),
                execution_time=self._calculate_execution_time(start_time)
            )
    
    async def _analyze_market_size(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis específico de tamaño de mercado"""
        prompt = MARKET_SIZE_PROMPT.format(**company_data)
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context=company_data,
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _identify_competitors(self, company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identificación de competidores principales"""
        prompt = COMPETITORS_PROMPT.format(**company_data)
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context=company_data,
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _analyze_trends(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis de tendencias del sector"""
        prompt = TRENDS_PROMPT.format(**company_data)
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context=company_data,
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response)
    
    async def _identify_opportunities(
        self, 
        company_data: Dict[str, Any],
        market_size: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identificación de oportunidades de mercado"""
        prompt = OPPORTUNITIES_PROMPT.format(**company_data)
        
        # Añadir contexto adicional para mejor análisis
        context = {
            **company_data,
            "market_size": market_size,
            "trends": trends
        }
        
        response = await self.ai_client.generate_structured_analysis(
            prompt=prompt,
            context=context,
            model=self.config.get("model", "gpt-4")
        )
        
        return json.loads(response) 