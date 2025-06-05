"""Prompts para el análisis primario de mercado"""

MARKET_SIZE_PROMPT = """
Analiza el tamaño del mercado para:
- Empresa: {company_name}
- Producto: {product_description}
- Mercado objetivo: {target_market}

Proporciona:
1. Tamaño total del mercado (en USD)
2. Tasa de crecimiento anual
3. Segmentos principales
4. Factores de crecimiento
"""

COMPETITORS_PROMPT = """
Identifica los competidores principales para:
- Empresa: {company_name}
- Producto: {product_description}
- Mercado objetivo: {target_market}

Para cada competidor, analiza:
1. Nombre y descripción
2. Cuota de mercado
3. Fortalezas principales
4. Debilidades identificadas
"""

TRENDS_PROMPT = """
Analiza las tendencias del mercado para:
- Empresa: {company_name}
- Producto: {product_description}
- Mercado objetivo: {target_market}

Identifica:
1. Tendencias tecnológicas
2. Tendencias de consumo
3. Tendencias regulatorias
4. Tendencias emergentes
"""

OPPORTUNITIES_PROMPT = """
Identifica oportunidades de mercado para:
- Empresa: {company_name}
- Producto: {product_description}
- Mercado objetivo: {target_market}

Considerando:
1. Nichos no atendidos
2. Cambios en el comportamiento del consumidor
3. Avances tecnológicos
4. Cambios regulatorios
""" 