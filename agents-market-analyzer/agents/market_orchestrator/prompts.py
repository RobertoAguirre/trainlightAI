"""Prompts para el agente orquestador de mercado"""

ORCHESTRATION_PROMPT = """
Orquesta el flujo de análisis de mercado.
Genera un plan de ejecución en formato JSON.

Estructura esperada:
{
    "plan_ejecucion": {
        "fases": [
            {
                "nombre": "fase1",
                "agentes": ["agente1", "agente2"],
                "dependencias": [],
                "tiempo_estimado": "valor"
            }
        ],
        "orden_ejecucion": ["fase1", "fase2"],
        "recursos_requeridos": ["recurso1", "recurso2"]
    },
    "configuracion": {
        "paralelismo": true/false,
        "tiempo_maximo": "valor",
        "reintentos": 3
    },
    "monitoreo": {
        "metricas": ["metrica1", "metrica2"],
        "alertas": ["alerta1", "alerta2"]
    }
}

Datos de entrada:
- company_name: {company_name}
- product_description: {product_description}
- target_market: {target_market}
- analysis_requirements: {analysis_requirements}
"""

VALIDATION_PROMPT = """
Valida el plan de orquestación.
Genera un reporte de validación en formato JSON.

Estructura esperada:
{
    "validacion": {
        "completitud": 0.95,
        "coherencia": 0.9,
        "viabilidad": 0.85
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
- orchestration_plan: {orchestration_plan}
- validation_context: {validation_context}
""" 