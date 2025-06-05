"""Prompts para el agente analizador de mercado"""

ANALYSIS_PROMPT = """
Analiza el mercado objetivo y genera un resumen ejecutivo.
Genera un reporte en formato JSON.

Estructura esperada:
{
    "resumen_ejecutivo": {
        "puntos_clave": ["punto1", "punto2"],
        "conclusiones": ["conclusion1", "conclusion2"],
        "recomendaciones": ["rec1", "rec2"]
    },
    "analisis_mercado": {
        "tamano": "valor",
        "crecimiento": "valor",
        "tendencias": ["tendencia1", "tendencia2"],
        "competidores": ["comp1", "comp2"]
    },
    "oportunidades": {
        "mercado": ["oportunidad1", "oportunidad2"],
        "producto": ["oportunidad1", "oportunidad2"]
    },
    "amenazas": {
        "mercado": ["amenaza1", "amenaza2"],
        "producto": ["amenaza1", "amenaza2"]
    }
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- market_data: {market_data}
"""

VALIDATION_PROMPT = """
Valida los resultados del análisis de mercado.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "completitud": 0.95,
        "precision": 0.9,
        "relevancia": 0.85
    },
    "problemas": [
        {
            "tipo": "tipo_problema",
            "descripcion": "descripcion_problema",
            "severidad": "alta/media/baja"
        }
    ],
    "sugerencias": [
        {
            "aspecto": "aspecto_afectado",
            "mejora": "descripcion_mejora"
        }
    ]
}

Datos de entrada:
- analysis_results: {analysis_results}
- validation_context: {validation_context}
""" 