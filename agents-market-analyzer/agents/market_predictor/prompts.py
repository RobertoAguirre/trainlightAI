"""Prompts para el agente predictor de mercado"""

PREDICTION_PROMPT = """
Genera predicciones de mercado basadas en el análisis.
Genera un reporte en formato JSON.

Estructura esperada:
{
    "predicciones": {
        "corto_plazo": {
            "tendencias": ["tendencia1", "tendencia2"],
            "metricas": {
                "crecimiento": "valor",
                "cuota_mercado": "valor"
            }
        },
        "medio_plazo": {
            "tendencias": ["tendencia1", "tendencia2"],
            "metricas": {
                "crecimiento": "valor",
                "cuota_mercado": "valor"
            }
        },
        "largo_plazo": {
            "tendencias": ["tendencia1", "tendencia2"],
            "metricas": {
                "crecimiento": "valor",
                "cuota_mercado": "valor"
            }
        }
    },
    "confianza": {
        "corto_plazo": 0.95,
        "medio_plazo": 0.85,
        "largo_plazo": 0.75
    },
    "factores_clave": {
        "positivos": ["factor1", "factor2"],
        "negativos": ["factor1", "factor2"]
    }
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- market_analysis: {market_analysis}
"""

VALIDATION_PROMPT = """
Valida las predicciones de mercado.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "confiabilidad": 0.95,
        "consistencia": 0.9,
        "fundamentacion": 0.85
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
- predictions: {predictions}
- validation_context: {validation_context}
""" 