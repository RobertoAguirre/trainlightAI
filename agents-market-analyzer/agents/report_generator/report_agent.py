"""Agente para generación de reportes finales"""
from typing import Dict, Any
from datetime import datetime
import time
import json
import io
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

from agents.base_agent import BaseMarketAgent, AgentResult
from integrations.openai_client import OpenAIClient
from .templates import REPORT_STRUCTURE

class ReportGeneratorAgent(BaseMarketAgent):
    """Agente para generación de reportes finales"""
    
    def __init__(self, config: Dict[str, Any]):
        # Configuración del cliente AI
        ai_client = OpenAIClient(config.get("openai_api_key"))
        super().__init__("report_generator", ai_client, config)
        
        # Crear directorio de reportes si no existe
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Generar reporte final basado en análisis previos
        
        Parámetros configurables en configs/agent_configs.py:
        - model: Modelo de OpenAI a utilizar
        - max_tokens: Máximo de tokens por respuesta
        - temperature: Temperatura para generación (0.1-1.0)
        """
        start_time = time.time()
        
        try:
            # Verificar análisis previos
            primary_results = self._get_primary_results(context)
            secondary_results = self._get_secondary_results(context)
            
            if not primary_results or not secondary_results:
                return AgentResult(
                    success=False,
                    data={},
                    error_message="Se requieren análisis primario y secundario completados",
                    execution_time=self._calculate_execution_time(start_time)
                )
            
            # Generar resumen ejecutivo
            executive_summary = await self._generate_executive_summary({
                "primary": primary_results,
                "secondary": secondary_results,
                "company": context["data"]
            })
            
            # Compilar reporte completo
            full_report = await self._compile_full_report(
                context,
                primary_results,
                secondary_results
            )
            
            # Generar PDF
            pdf_path = self._generate_pdf(full_report, context["session_id"])
            
            results = {
                "executive_summary": executive_summary,
                "report_path": str(pdf_path),
                "generation_date": datetime.now().isoformat()
            }
            
            return AgentResult(
                success=True,
                data=results,
                execution_time=self._calculate_execution_time(start_time),
                metadata={
                    "model_used": self.config.get("model", "gpt-4"),
                    "pdf_size": pdf_path.stat().st_size
                }
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
    
    def _get_secondary_results(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener resultados del análisis secundario"""
        return context.get("agent_triggers", {}).get("secondary_analysis", {}).get("result", {})
    
    async def _generate_executive_summary(self, analyses: Dict[str, Any]) -> str:
        """Generar resumen ejecutivo del reporte"""
        prompt = f"""
        Genera un resumen ejecutivo conciso basado en:
        
        Datos de la empresa:
        {json.dumps(analyses['company'], indent=2)}
        
        Análisis primario:
        {json.dumps(analyses['primary'], indent=2)}
        
        Análisis secundario:
        {json.dumps(analyses['secondary'], indent=2)}
        
        Enfócate en:
        1. Hallazgos más importantes
        2. Oportunidades clave
        3. Riesgos principales
        4. Recomendaciones críticas
        """
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=analyses,
            model=self.config.get("model", "gpt-4")
        )
        
        return response
    
    async def _compile_full_report(
        self,
        context: Dict[str, Any],
        primary_results: Dict[str, Any],
        secondary_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compilar reporte completo en formato estructurado"""
        return {
            "title": REPORT_STRUCTURE["title"].format(
                company_name=context["data"]["company_name"]
            ),
            "sections": [
                {
                    "title": section["title"],
                    "content": section["template"].format(
                        company_name=context["data"]["company_name"],
                        analysis_date=datetime.now().strftime("%Y-%m-%d"),
                        market_size=primary_results["market_size"],
                        key_points=await self._extract_key_points(primary_results, secondary_results),
                        main_recommendations=await self._extract_main_recommendations(secondary_results),
                        confidence_score=secondary_results["confidence_score"],
                        validated_sources=await self._get_validated_sources(secondary_results),
                        market_size_section=await self._format_market_size(primary_results),
                        competitors_section=await self._format_competitors(primary_results),
                        trends_section=await self._format_trends(primary_results),
                        opportunities_section=await self._format_opportunities(primary_results),
                        strengths="\n".join(f"- {s}" for s in secondary_results["swot_analysis"]["strengths"]),
                        weaknesses="\n".join(f"- {w}" for w in secondary_results["swot_analysis"]["weaknesses"]),
                        opportunities="\n".join(f"- {o}" for o in secondary_results["swot_analysis"]["opportunities"]),
                        threats="\n".join(f"- {t}" for t in secondary_results["swot_analysis"]["threats"]),
                        **secondary_results["financial_projections"],
                        break_even_analysis=secondary_results["financial_projections"].get("break_even", "N/A"),
                        roi_analysis=secondary_results["financial_projections"].get("roi", "N/A"),
                        entry_strategy=secondary_results["strategic_recommendations"]["entry_strategy"],
                        growth_plan=secondary_results["strategic_recommendations"]["growth_plan"],
                        risk_mitigation=secondary_results["strategic_recommendations"]["risk_mitigation"],
                        kpis=secondary_results["strategic_recommendations"].get("kpis", "N/A")
                    ),
                    "page_break_after": section["page_break_after"]
                }
                for section in REPORT_STRUCTURE["sections"]
            ]
        }
    
    def _generate_pdf(self, report_data: Dict[str, Any], session_id: str) -> Path:
        """Generar PDF del reporte"""
        pdf_path = self.reports_dir / f"market_report_{session_id}.pdf"
        
        # Configurar estilos
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        ))
        
        # Crear documento
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Preparar contenido
        story = []
        
        # Título
        story.append(Paragraph(report_data["title"], styles["CustomTitle"]))
        story.append(Spacer(1, 12))
        
        # Secciones
        for section in report_data["sections"]:
            story.append(Paragraph(section["title"], styles["Heading1"]))
            story.append(Spacer(1, 12))
            
            # Dividir contenido en párrafos
            paragraphs = section["content"].split("\n\n")
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para, styles["Normal"]))
                    story.append(Spacer(1, 12))
            
            if section["page_break_after"]:
                story.append(PageBreak())
        
        # Generar PDF
        doc.build(story)
        return pdf_path
    
    async def _extract_key_points(self, primary: Dict[str, Any], secondary: Dict[str, Any]) -> str:
        """Extraer puntos clave de los análisis"""
        prompt = f"""
        Extrae los 3-5 puntos más importantes de:
        
        Análisis primario:
        {json.dumps(primary, indent=2)}
        
        Análisis secundario:
        {json.dumps(secondary, indent=2)}
        
        Formato: Lista numerada
        """
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context={"primary": primary, "secondary": secondary},
            model=self.config.get("model", "gpt-4")
        )
        
        return response
    
    async def _extract_main_recommendations(self, secondary: Dict[str, Any]) -> str:
        """Extraer recomendaciones principales"""
        prompt = f"""
        Extrae las 3 recomendaciones más importantes de:
        
        {json.dumps(secondary["strategic_recommendations"], indent=2)}
        
        Formato: Lista numerada
        """
        
        response = await self.ai_client.analyze(
            prompt=prompt,
            context=secondary,
            model=self.config.get("model", "gpt-4")
        )
        
        return response
    
    async def _get_validated_sources(self, secondary: Dict[str, Any]) -> str:
        """Obtener fuentes validadas"""
        return ", ".join(secondary["validation"].get("validated_sources", ["N/A"]))
    
    async def _format_market_size(self, primary: Dict[str, Any]) -> str:
        """Formatear sección de tamaño de mercado"""
        market_size = primary["market_size"]
        return f"""
        Tamaño total: ${market_size['total_size']:,.2f}
        Crecimiento anual: {market_size['growth_rate']:.1%}
        Segmentos principales: {', '.join(market_size['segments'])}
        """
    
    async def _format_competitors(self, primary: Dict[str, Any]) -> str:
        """Formatear sección de competidores"""
        competitors = primary["competitors"]
        return "\n\n".join(
            f"• {comp['name']} ({comp['market_share']:.1%} del mercado)\n"
            f"  Fortalezas: {', '.join(comp['strengths'])}\n"
            f"  Debilidades: {', '.join(comp['weaknesses'])}"
            for comp in competitors
        )
    
    async def _format_trends(self, primary: Dict[str, Any]) -> str:
        """Formatear sección de tendencias"""
        trends = primary["trends"]
        return "\n".join(
            f"• {category}: {', '.join(trends[category])}"
            for category in ["technological", "consumer", "regulatory", "emerging"]
        )
    
    async def _format_opportunities(self, primary: Dict[str, Any]) -> str:
        """Formatear sección de oportunidades"""
        opportunities = primary["opportunities"]
        return "\n".join(
            f"• {category}: {', '.join(opportunities[category])}"
            for category in ["untapped_niches", "consumer_changes", "tech_advances", "regulatory_changes"]
        ) 