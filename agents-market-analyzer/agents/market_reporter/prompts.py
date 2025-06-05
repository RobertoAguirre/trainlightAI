"""Prompts para el agente reportero de mercado"""

REPORT_GENERATION_PROMPT = """
Genera un reporte de análisis de mercado en formato JSON.

Estructura esperada:
{
    "resumen_ejecutivo": {
        "puntos_clave": ["punto1", "punto2"],
        "conclusiones": ["conclusion1", "conclusion2"],
        "recomendaciones": ["rec1", "rec2"]
    },
    "analisis_detallado": {
        "tendencias": ["tendencia1", "tendencia2"],
        "oportunidades": ["oportunidad1", "oportunidad2"],
        "amenazas": ["amenaza1", "amenaza2"]
    },
    "metricas": {
        "tamano_mercado": "valor",
        "tasa_crecimiento": "valor",
        "cuota_mercado": "valor"
    }
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- analysis_results: {analysis_results}
"""

REPORT_VALIDATION_PROMPT = """
Valida el reporte de análisis de mercado.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "completitud": 0.95,
        "claridad": 0.9,
        "precision": 0.85
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
            "seccion": "seccion_afectada",
            "mejora": "descripcion_mejora"
        }
    ]
}

Datos de entrada:
- report: {report}
- context: {context}
"""

REPORT_FORMAT_PROMPT = """
Formatea el reporte de mercado en formato JSON con la siguiente estructura:
{
    "formato": {
        "tipo": "pdf/markdown",
        "estilo": "profesional/minimalista",
        "idioma": "es"
    },
    "secciones": [
        {
            "titulo": "string",
            "contenido": "string",
            "orden": number
        }
    ],
    "graficos": [
        {
            "tipo": "string",
            "datos": "string",
            "posicion": number
        }
    ]
}

Datos de entrada:
- Reporte: {report_data}
- Preferencias: {format_preferences}
""" 