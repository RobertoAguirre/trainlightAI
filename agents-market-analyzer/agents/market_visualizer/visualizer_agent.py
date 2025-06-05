"""Agente visualizador de mercado"""
from typing import Dict, Any
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from agents.base_agent import BaseMarketAgent
from agents.market_visualizer.prompts import VISUALIZATION_PROMPT, DASHBOARD_PROMPT

class MarketVisualizerAgent(BaseMarketAgent):
    """Agente para visualizar datos de mercado"""
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializa el agente visualizador"""
        super().__init__(config)
        self.visualization_config = {
            "default_theme": config.get("default_theme", "light"),
            "default_colors": config.get("default_colors", ["#1f77b4", "#ff7f0e", "#2ca02c"]),
            "default_font": config.get("default_font", "Arial")
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la visualización de datos"""
        try:
            # Validar contexto
            self._validate_context(context)
            
            # Generar visualización
            if context.get("visualization_type") == "dashboard":
                visualization = await self._generate_dashboard(context)
            else:
                visualization = await self._generate_visualization(context)
            
            # Crear gráfico
            chart = self._create_chart(visualization)
            
            # Compilar resultados
            return {
                "success": True,
                "data": {
                    "visualization": visualization,
                    "chart": chart,
                    "metadata": {
                        "visualization_time": datetime.now().isoformat(),
                        "config": self.visualization_config
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
    
    async def _generate_visualization(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Genera una visualización individual"""
        prompt = VISUALIZATION_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            market_data=json.dumps(context.get("market_data", {})),
            visualization_type=context.get("visualization_type", "line")
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    async def _generate_dashboard(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un dashboard de visualizaciones"""
        prompt = DASHBOARD_PROMPT.format(
            company_name=context["data"]["company_name"],
            product_description=context["data"]["product_description"],
            target_market=context["data"]["target_market"],
            market_data=json.dumps(context.get("market_data", {})),
            dashboard_type=context.get("dashboard_type", "standard")
        )
        
        response = await self.ai_client.analyze(prompt)
        return json.loads(response)
    
    def _create_chart(self, visualization: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un gráfico basado en la configuración"""
        if "layout" in visualization:  # Dashboard
            return self._create_dashboard(visualization)
        else:  # Gráfico individual
            return self._create_single_chart(visualization)
    
    def _create_single_chart(self, visualization: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un gráfico individual"""
        config = visualization["configuracion"]
        tipo = visualization["tipo_grafico"]
        
        if tipo == "linea":
            fig = px.line(
                x=config["ejes"]["x"]["datos"],
                y=config["ejes"]["y"]["datos"],
                title=config["titulo"]
            )
        elif tipo == "barras":
            fig = px.bar(
                x=config["ejes"]["x"]["datos"],
                y=config["ejes"]["y"]["datos"],
                title=config["titulo"]
            )
        elif tipo == "dispersión":
            fig = px.scatter(
                x=config["ejes"]["x"]["datos"],
                y=config["ejes"]["y"]["datos"],
                title=config["titulo"]
            )
        elif tipo == "pie":
            fig = px.pie(
                values=config["ejes"]["y"]["datos"],
                names=config["ejes"]["x"]["datos"],
                title=config["titulo"]
            )
        elif tipo == "heatmap":
            fig = px.imshow(
                config["ejes"]["y"]["datos"],
                title=config["titulo"]
            )
        
        # Aplicar estilo
        fig.update_layout(
            template=visualization["estilo"]["tema"],
            font_family=visualization["estilo"]["fuente"]
        )
        
        return fig.to_json()
    
    def _create_dashboard(self, dashboard: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un dashboard de visualizaciones"""
        layout = dashboard["layout"]
        fig = make_subplots(
            rows=layout["filas"],
            cols=layout["columnas"],
            subplot_titles=[g["configuracion"]["titulo"] for g in dashboard["graficos"]]
        )
        
        for i, grafico in enumerate(dashboard["graficos"]):
            row = grafico["posicion"]["fila"] + 1
            col = grafico["posicion"]["columna"] + 1
            
            if grafico["tipo"] == "linea":
                fig.add_trace(
                    go.Scatter(
                        x=grafico["configuracion"]["ejes"]["x"]["datos"],
                        y=grafico["configuracion"]["ejes"]["y"]["datos"],
                        name=grafico["configuracion"]["series"][0]["nombre"]
                    ),
                    row=row,
                    col=col
                )
            # Agregar más tipos de gráficos según sea necesario
        
        # Aplicar estilo
        fig.update_layout(
            template=dashboard["estilo"]["tema"],
            font_family=dashboard["estilo"]["fuente"],
            title_text=dashboard["titulo"]
        )
        
        return fig.to_json() 