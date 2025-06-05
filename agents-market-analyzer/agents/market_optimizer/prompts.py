"""Prompts para el agente optimizador de mercado"""

OPTIMIZATION_PROMPT = """
Optimiza los cálculos y análisis de mercado para:
Empresa: {company_name}
Producto: {product_description}
Mercado objetivo: {target_market}

Considera:
1. Precisión de cálculos
2. Eficiencia computacional
3. Validación de datos
4. Optimización de recursos

Formato de respuesta: JSON estructurado
"""

CALCULATION_OPTIMIZATION_PROMPT = """
Optimiza los cálculos de mercado para:
Datos: {market_data}

Enfócate en:
1. Algoritmos eficientes
2. Precisión numérica
3. Manejo de errores
4. Validación de resultados

Formato de respuesta: JSON estructurado
"""

PERFORMANCE_OPTIMIZATION_PROMPT = """
Optimiza el rendimiento del análisis para:
Métricas: {metrics}
Datos: {data_points}

Considera:
1. Tiempo de ejecución
2. Uso de memoria
3. Paralelización
4. Caché de resultados

Formato de respuesta: JSON estructurado
"""

VALIDATION_OPTIMIZATION_PROMPT = """
Optimiza la validación de datos para:
Análisis: {analysis_data}

Enfócate en:
1. Verificación de integridad
2. Consistencia de datos
3. Detección de anomalías
4. Corrección de errores

Formato de respuesta: JSON estructurado
""" 