"""Prompts para el agente exportador de mercado"""

EXPORT_FORMAT_PROMPT = """
Formatea los resultados del análisis para exportación.
Genera un reporte en formato JSON.

Estructura esperada:
{
    "formato": {
        "tipo": "json/csv/excel",
        "estructura": {
            "secciones": ["seccion1", "seccion2"],
            "campos": ["campo1", "campo2"]
        }
    },
    "datos": {
        "resumen": {
            "puntos_clave": ["punto1", "punto2"],
            "conclusiones": ["conclusion1", "conclusion2"]
        },
        "metricas": {
            "tamano_mercado": "valor",
            "tasa_crecimiento": "valor"
        }
    }
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- analysis_results: {analysis_results}
- export_format: {export_format}
"""

EXPORT_VALIDATION_PROMPT = """
Valida el formato de exportación.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "formato_correcto": true,
        "datos_completos": true,
        "estructura_valida": true
    },
    "errores": [
        {
            "tipo": "tipo_error",
            "descripcion": "descripcion_error",
            "ubicacion": "seccion_afectada"
        }
    ],
    "sugerencias": [
        {
            "campo": "campo_afectado",
            "mejora": "descripcion_mejora"
        }
    ]
}

Datos de entrada:
- export_data: {export_data}
- format_requirements: {format_requirements}
""" 