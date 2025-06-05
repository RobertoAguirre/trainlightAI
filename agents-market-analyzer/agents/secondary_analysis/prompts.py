"""Prompts para el análisis secundario de mercado"""

VALIDATION_PROMPT = """
Valida y contrasta los datos del análisis primario:

Datos de la empresa:
{company_data}

Resultados del análisis primario:
{primary_results}

Evalúa:
1. Consistencia de datos
2. Fuentes de información
3. Métodos de análisis
4. Confiabilidad de resultados
"""

SWOT_PROMPT = """
Realiza un análisis SWOT detallado:

Datos de la empresa:
{company_data}

Análisis de mercado:
{market_analysis}

Analiza:
1. Fortalezas internas
2. Debilidades internas
3. Oportunidades externas
4. Amenazas externas
"""

FINANCIAL_PROMPT = """
Genera proyecciones financieras:

Datos del mercado:
{market_analysis}

Considera:
1. Ingresos proyectados (3 años)
2. Costos estimados
3. Punto de equilibrio
4. ROI esperado
"""

STRATEGIC_PROMPT = """
Desarrolla recomendaciones estratégicas:

Datos de la empresa:
{company_data}

Análisis previos:
{previous_analyses}

Proporciona:
1. Estrategias de entrada
2. Plan de crecimiento
3. Mitigación de riesgos
4. KPIs recomendados
""" 