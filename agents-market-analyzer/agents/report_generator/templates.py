"""Plantillas para la generación de reportes"""

EXECUTIVE_SUMMARY_TEMPLATE = """
Resumen Ejecutivo - Análisis de Mercado

Empresa: {company_name}
Fecha: {analysis_date}

1. Resumen del Mercado
-------------------
Tamaño total: ${market_size[total_size]:,.2f}
Crecimiento anual: {market_size[growth_rate]:.1%}
Segmentos principales: {market_size[segments]}

2. Puntos Clave
-------------
{key_points}

3. Recomendaciones Principales
---------------------------
{main_recommendations}

4. Métricas de Confianza
----------------------
Score de confianza: {confidence_score:.1%}
Fuentes validadas: {validated_sources}
"""

MARKET_ANALYSIS_TEMPLATE = """
Análisis de Mercado Detallado

1. Tamaño y Crecimiento
---------------------
{market_size_section}

2. Competidores
-------------
{competitors_section}

3. Tendencias
-----------
{trends_section}

4. Oportunidades
--------------
{opportunities_section}
"""

SWOT_ANALYSIS_TEMPLATE = """
Análisis SWOT

Fortalezas:
{strengths}

Debilidades:
{weaknesses}

Oportunidades:
{opportunities}

Amenazas:
{threats}
"""

FINANCIAL_PROJECTIONS_TEMPLATE = """
Proyecciones Financieras

1. Ingresos Proyectados
--------------------
Año 1: ${year_1:,.2f}
Año 2: ${year_2:,.2f}
Año 3: ${year_3:,.2f}

2. Punto de Equilibrio
--------------------
{break_even_analysis}

3. ROI Esperado
-------------
{roi_analysis}
"""

STRATEGIC_RECOMMENDATIONS_TEMPLATE = """
Recomendaciones Estratégicas

1. Estrategia de Entrada
---------------------
{entry_strategy}

2. Plan de Crecimiento
--------------------
{growth_plan}

3. Mitigación de Riesgos
----------------------
{risk_mitigation}

4. KPIs Recomendados
-----------------
{kpis}
"""

REPORT_STRUCTURE = {
    "title": "Análisis de Mercado - {company_name}",
    "sections": [
        {
            "title": "Resumen Ejecutivo",
            "template": EXECUTIVE_SUMMARY_TEMPLATE,
            "page_break_after": True
        },
        {
            "title": "Análisis de Mercado",
            "template": MARKET_ANALYSIS_TEMPLATE,
            "page_break_after": True
        },
        {
            "title": "Análisis SWOT",
            "template": SWOT_ANALYSIS_TEMPLATE,
            "page_break_after": True
        },
        {
            "title": "Proyecciones Financieras",
            "template": FINANCIAL_PROJECTIONS_TEMPLATE,
            "page_break_after": True
        },
        {
            "title": "Recomendaciones Estratégicas",
            "template": STRATEGIC_RECOMMENDATIONS_TEMPLATE,
            "page_break_after": False
        }
    ]
} 