"""Prompts para el agente de datos de mercado"""

MARKET_DATA_PROMPT = """
Analiza y extrae datos relevantes del mercado para:
Empresa: {company_name}
Producto: {product_description}
Mercado objetivo: {target_market}

Proporciona un análisis estructurado que incluya:
1. Métricas clave del mercado
2. Tendencias actuales
3. Datos demográficos relevantes
4. Indicadores económicos

Formato de respuesta: JSON estructurado
"""

INDUSTRY_METRICS_PROMPT = """
Extrae métricas específicas de la industria para:
Sector: {industry}
Región: {region}

Incluye:
1. Tasa de crecimiento anual
2. Margen promedio del sector
3. Tamaño total del mercado
4. Principales segmentos

Formato de respuesta: JSON estructurado
"""

CONSUMER_BEHAVIOR_PROMPT = """
Analiza el comportamiento del consumidor para:
Producto: {product_description}
Mercado objetivo: {target_market}

Considera:
1. Patrones de compra
2. Preferencias de precio
3. Factores de decisión
4. Tendencias de consumo

Formato de respuesta: JSON estructurado
"""

COMPETITIVE_LANDSCAPE_PROMPT = """
Mapea el panorama competitivo para:
Empresa: {company_name}
Sector: {industry}

Analiza:
1. Principales competidores
2. Cuota de mercado
3. Estrategias competitivas
4. Barreras de entrada

Formato de respuesta: JSON estructurado
""" 