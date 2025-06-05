"""Prompts para el agente validador de mercado"""

VALIDATION_PROMPT = """
Valida los resultados del análisis de mercado.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "completitud": 0.95,
        "consistencia": 0.9,
        "confiabilidad": 0.85
    },
    "errores": [
        {
            "tipo": "tipo_error",
            "descripcion": "descripcion_error",
            "severidad": "alta/media/baja",
            "ubicacion": "seccion_afectada"
        }
    ],
    "advertencias": [
        {
            "tipo": "tipo_advertencia",
            "descripcion": "descripcion_advertencia",
            "impacto": "alto/medio/bajo"
        }
    ]
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- analysis_results: {analysis_results}
"""

CORRECTION_PROMPT = """
Genera correcciones para los errores encontrados.
Genera un reporte de correcciones en formato JSON.

Estructura esperada:
{
    "correcciones": [
        {
            "error": "descripcion_error",
            "correccion": "descripcion_correccion",
            "prioridad": "alta/media/baja"
        }
    ],
    "resultado_corregido": {
        "seccion": "nombre_seccion",
        "valor_original": "valor_original",
        "valor_corregido": "valor_corregido"
    }
}

Datos de entrada:
- validation_results: {validation_results}
- context: {context}
""" 