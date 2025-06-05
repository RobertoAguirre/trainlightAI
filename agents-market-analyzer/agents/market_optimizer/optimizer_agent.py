"""Agente para optimización de cálculos y análisis de mercado"""
from typing import Dict, Any, List
import time
import json
from datetime import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import asyncio

from agents.base_agent import BaseMarketAgent, AgentResult
from integrations.openai_client import OpenAIClient
from .prompts import (
    OPTIMIZATION_PROMPT,
    CALCULATION_OPTIMIZATION_PROMPT,
    PERFORMANCE_OPTIMIZATION_PROMPT,
    VALIDATION_OPTIMIZATION_PROMPT
)

class MarketOptimizerAgent(BaseMarketAgent):
    """Agente para optimización de cálculos y análisis de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        # Configuración del cliente AI
        ai_client = OpenAIClient(config.get("openai_api_key"))
        super().__init__("market_optimizer", ai_client, config)
        
        # Configuración de optimización
        self.max_workers = config.get("max_workers", 4)
        self.cache_size = config.get("cache_size", 1000)
        self.precision = config.get("precision", 6)
        
        # Inicializar caché
        self._init_cache()
    
    def _init_cache(self):
        """Inicializar caché de resultados"""
        self.cache = {}
        self.cache_timestamps = {}
    
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Ejecuta la optimización de cálculos y análisis
        
        Parámetros configurables en configs/agent_configs.py:
        - model: Modelo de OpenAI a utilizar
        - max_tokens: Máximo de tokens por respuesta
        - temperature: Temperatura para generación (0.1-1.0)
        - max_workers: Número máximo de workers para paralelización
        - cache_size: Tamaño máximo del caché
        - precision: Precisión decimal para cálculos
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
            
            # Optimizar cálculos
            calculation_optimization = await self._optimize_calculations(context)
            
            # Optimizar rendimiento
            performance_optimization = await self._optimize_performance(context)
            
            # Optimizar validación
            validation_optimization = await self._optimize_validation(context)
            
            # Aplicar optimizaciones
            optimized_results = await self._apply_optimizations(
                context,
                calculation_optimization,
                performance_optimization,
                validation_optimization
            )
            
            # Compilar resultados
            results = {
                "optimizations": {
                    "calculations": calculation_optimization,
                    "performance": performance_optimization,
                    "validation": validation_optimization
                },
                "optimized_results": optimized_results,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "execution_time": self._calculate_execution_time(start_time),
                    "memory_usage": self._get_memory_usage(),
                    "cache_hits": self._get_cache_stats()["hits"],
                    "cache_misses": self._get_cache_stats()["misses"]
                }
            }
            
            return AgentResult(
                success=True,
                data=results,
                execution_time=self._calculate_execution_time(start_time),
                metadata={
                    "model_used": self.config.get("model", "gpt-4"),
                    "optimization_level": self._calculate_optimization_level(results)
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
    
    async def _optimize_calculations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar cálculos de mercado"""
        # Verificar caché
        cache_key = f"calc_opt_{hash(str(context['data']))}"
        if cache_key in self.cache:
            self.cache_timestamps[cache_key] = time.time()
            return self.cache[cache_key]
        
        prompt = CALCULATION_OPTIMIZATION_PROMPT.format(
            market_data=json.dumps(context["data"])
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        result = json.loads(response)
        self._update_cache(cache_key, result)
        return result
    
    async def _optimize_performance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar rendimiento del análisis"""
        # Verificar caché
        cache_key = f"perf_opt_{hash(str(context['data']))}"
        if cache_key in self.cache:
            self.cache_timestamps[cache_key] = time.time()
            return self.cache[cache_key]
        
        prompt = PERFORMANCE_OPTIMIZATION_PROMPT.format(
            metrics=json.dumps(context.get("metrics", {})),
            data_points=len(context["data"])
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        result = json.loads(response)
        self._update_cache(cache_key, result)
        return result
    
    async def _optimize_validation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar validación de datos"""
        # Verificar caché
        cache_key = f"val_opt_{hash(str(context['data']))}"
        if cache_key in self.cache:
            self.cache_timestamps[cache_key] = time.time()
            return self.cache[cache_key]
        
        prompt = VALIDATION_OPTIMIZATION_PROMPT.format(
            analysis_data=json.dumps(context.get("analysis", {}))
        )
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=context["data"],
            model=self.config.get("model", "gpt-4")
        )
        
        result = json.loads(response)
        self._update_cache(cache_key, result)
        return result
    
    async def _apply_optimizations(
        self,
        context: Dict[str, Any],
        calculation_opt: Dict[str, Any],
        performance_opt: Dict[str, Any],
        validation_opt: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aplicar optimizaciones a los datos"""
        # Paralelizar procesamiento
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Procesar cálculos optimizados
            calc_future = executor.submit(
                self._process_calculations,
                context["data"],
                calculation_opt
            )
            
            # Procesar validaciones optimizadas
            val_future = executor.submit(
                self._process_validations,
                context["data"],
                validation_opt
            )
            
            # Esperar resultados
            calc_results = calc_future.result()
            val_results = val_future.result()
        
        # Aplicar optimizaciones de rendimiento
        optimized_data = self._apply_performance_optimizations(
            calc_results,
            performance_opt
        )
        
        # Validar resultados finales
        validated_results = self._validate_optimized_results(
            optimized_data,
            val_results
        )
        
        return validated_results
    
    def _process_calculations(self, data: Dict[str, Any], optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar cálculos con optimizaciones"""
        results = {}
        
        # Aplicar optimizaciones numéricas
        for key, value in data.items():
            if isinstance(value, (int, float)):
                results[key] = np.round(value, self.precision)
            else:
                results[key] = value
        
        return results
    
    def _process_validations(self, data: Dict[str, Any], optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar validaciones con optimizaciones"""
        results = {}
        
        # Aplicar validaciones optimizadas
        for key, value in data.items():
            if self._validate_value(value, optimization):
                results[key] = value
        
        return results
    
    def _apply_performance_optimizations(
        self,
        data: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aplicar optimizaciones de rendimiento"""
        # Implementar optimizaciones específicas
        optimized_data = data.copy()
        
        # Optimizar estructuras de datos
        if optimization.get("use_numpy", False):
            for key, value in optimized_data.items():
                if isinstance(value, list):
                    optimized_data[key] = np.array(value)
        
        return optimized_data
    
    def _validate_optimized_results(
        self,
        data: Dict[str, Any],
        validation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validar resultados optimizados"""
        validated_data = {}
        
        # Aplicar validaciones
        for key, value in data.items():
            if self._validate_value(value, validation):
                validated_data[key] = value
        
        return validated_data
    
    def _validate_value(self, value: Any, validation: Dict[str, Any]) -> bool:
        """Validar un valor según las reglas de optimización"""
        # Implementar validaciones específicas
        if validation.get("check_numeric", False):
            if not isinstance(value, (int, float, np.number)):
                return False
        
        if validation.get("check_range", False):
            min_val = validation.get("min_value", float("-inf"))
            max_val = validation.get("max_value", float("inf"))
            if not (min_val <= value <= max_val):
                return False
        
        return True
    
    def _update_cache(self, key: str, value: Any):
        """Actualizar caché de resultados"""
        # Limpiar caché si es necesario
        if len(self.cache) >= self.cache_size:
            oldest_key = min(self.cache_timestamps.items(), key=lambda x: x[1])[0]
            del self.cache[oldest_key]
            del self.cache_timestamps[oldest_key]
        
        # Actualizar caché
        self.cache[key] = value
        self.cache_timestamps[key] = time.time()
    
    def _get_cache_stats(self) -> Dict[str, int]:
        """Obtener estadísticas del caché"""
        return {
            "hits": sum(1 for _ in self.cache_timestamps.values()),
            "misses": len(self.cache) - len(self.cache_timestamps)
        }
    
    def _get_memory_usage(self) -> int:
        """Obtener uso de memoria en bytes"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss
    
    def _calculate_optimization_level(self, results: Dict[str, Any]) -> float:
        """Calcular nivel de optimización alcanzado"""
        metrics = results.get("metrics", {})
        if not metrics:
            return 0.0
        
        # Calcular score basado en métricas
        execution_time = metrics.get("execution_time", 0)
        memory_usage = metrics.get("memory_usage", 0)
        cache_hits = metrics.get("cache_hits", 0)
        
        # Normalizar métricas
        time_score = 1.0 / (1.0 + execution_time)
        memory_score = 1.0 / (1.0 + memory_usage / 1e6)  # Normalizar a MB
        cache_score = cache_hits / (cache_hits + 1)
        
        # Calcular score final
        return (time_score + memory_score + cache_score) / 3.0 