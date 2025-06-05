"""Prompts para el agente integrador de mercado"""

INTEGRATION_PROMPT = """
Integra los resultados de análisis de mercado.
Genera un reporte en formato JSON.

Estructura esperada:
{
    "resumen_integrado": {
        "puntos_clave": ["punto1", "punto2"],
        "conclusiones": ["conclusion1", "conclusion2"],
        "recomendaciones": ["recomendacion1", "recomendacion2"]
    },
    "analisis_combinado": {
        "tendencias": ["tendencia1", "tendencia2"],
        "metricas": {
            "crecimiento": "valor",
            "cuota_mercado": "valor"
        },
        "riesgos": ["riesgo1", "riesgo2"]
    },
    "metricas_consolidadas": {
        "confianza": 0.95,
        "consistencia": 0.9,
        "relevancia": 0.85
    }
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- analysis_results: {analysis_results}
"""

CONSISTENCY_CHECK_PROMPT = """
Verifica la consistencia de los resultados integrados.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "consistencia": 0.95,
        "coherencia": 0.9,
        "confiabilidad": 0.85
    },
    "inconsistencias": [
        {
            "tipo": "tipo_inconsistencia",
            "descripcion": "descripcion_inconsistencia",
            "severidad": "alta/media/baja"
        }
    ],
    "ajustes": [
        {
            "aspecto": "aspecto_afectado",
            "sugerencia": "descripcion_ajuste"
        }
    ]
}

Datos de entrada:
- integrated_results: {integrated_results}
- validation_context: {validation_context}
""" 