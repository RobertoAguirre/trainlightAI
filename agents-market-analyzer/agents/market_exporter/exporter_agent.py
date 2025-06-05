"""Agente exportador de mercado"""
from typing import Dict, Any
import json
import os
import pandas as pd
from datetime import datetime

from agents.base_agent import BaseMarketAgent
from agents.market_exporter.prompts import EXPORT_FORMAT_PROMPT, EXPORT_VALIDATION_PROMPT
from utils.ai_client import OpenAIClient

class MarketExporterAgent(BaseMarketAgent):
    """Agente para exportar análisis de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente exportador"""
        super().__init__(config)
        self.ai_client = OpenAIClient(
            api_key=config["openai_api_key"],
            model=config.get("model", "gpt-4"),
            max_tokens=config.get("max_tokens", 2000),
            temperature=config.get("temperature", 0.7)
        )
        self.export_config = {
            "output_dir": config.get("output_dir", "exports"),
            "default_format": config.get("default_format", "json"),
            "date_format": config.get("date_format", "%Y%m%d_%H%M%S")
        }
        
        # Crear directorio de salida si no existe
        os.makedirs(self.export_config["output_dir"], exist_ok=True)
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la exportación del análisis"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Formatear datos
            export_data = await self._format_export(context)
            
            # Validar formato
            validation = await self._validate_export(export_data, context)
            
            # Exportar datos
            export_path = await self._export_data(export_data, context)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "export_data": export_data,
                    "validation": validation,
                    "export_path": export_path,
                    "metadata": {
                        "export_time": datetime.now().isoformat(),
                        "config": self.export_config
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
    
    async def _format_export(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Formatea los datos para exportación"""
        prompt = EXPORT_FORMAT_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            analysis_results=json.dumps(context.get("analysis_results", {})),
            export_format=context.get("export_format", self.export_config["default_format"])
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _validate_export(self, export_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Valida el formato de exportación"""
        prompt = EXPORT_VALIDATION_PROMPT.format(
            export_data=json.dumps(export_data),
            format_requirements=json.dumps(context.get("format_requirements", {}))
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _export_data(self, export_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Exporta los datos al formato especificado"""
        format_type = context.get("export_format", self.export_config["default_format"])
        timestamp = datetime.now().strftime(self.export_config["date_format"])
        filename = f"market_analysis_{timestamp}"
        
        if format_type == "json":
            filepath = os.path.join(self.export_config["output_dir"], f"{filename}.json")
            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2)
        
        elif format_type == "csv":
            filepath = os.path.join(self.export_config["output_dir"], f"{filename}.csv")
            df = pd.DataFrame(export_data["datos"])
            df.to_csv(filepath, index=False)
        
        elif format_type == "excel":
            filepath = os.path.join(self.export_config["output_dir"], f"{filename}.xlsx")
            with pd.ExcelWriter(filepath) as writer:
                for section, data in export_data["datos"].items():
                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name=section, index=False)
        
        else:
            raise ValueError(f"Formato no soportado: {format_type}")
        
        return filepath 