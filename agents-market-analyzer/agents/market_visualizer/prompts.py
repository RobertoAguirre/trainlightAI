"""Prompts para el agente visualizador de mercado"""

VISUALIZATION_PROMPT = """
Analiza los datos de mercado y genera una descripción detallada de las visualizaciones necesarias.

Datos de entrada:
- Empresa: {company_name}
- Producto: {product_description}
- Mercado objetivo: {target_market}
- Datos de análisis: {analysis_data}

Genera una respuesta en formato JSON con la siguiente estructura:
{{
    "charts": [
        {{
            "type": "tipo de gráfico",
            "title": "título",
            "description": "descripción",
            "data_points": ["punto1", "punto2"],
            "metrics": ["métrica1", "métrica2"],
            "style": {{
                "colors": ["color1", "color2"],
                "layout": "vertical/horizontal",
                "annotations": ["anotación1", "anotación2"]
            }}
        }}
    ],
    "dashboards": [
        {{
            "title": "título del dashboard",
            "description": "descripción",
            "layout": "grid/flow",
            "components": ["componente1", "componente2"],
            "interactions": ["interacción1", "interacción2"]
        }}
    ],
    "recommendations": [
        {{
            "visualization_type": "tipo",
            "reason": "razón",
            "priority": "alta/media/baja"
        }}
    ]
}}
"""

CHART_CONFIG_PROMPT = """
Configura los parámetros específicos para la generación de gráficos.

Datos de entrada:
- Tipo de gráfico: {chart_type}
- Datos: {data}
- Contexto: {context}

Genera una respuesta en formato JSON con la siguiente estructura:
{{
    "chart_config": {{
        "type": "tipo de gráfico",
        "data": {{
            "x": ["valor1", "valor2"],
            "y": ["valor1", "valor2"],
            "series": ["serie1", "serie2"]
        }},
        "style": {{
            "colors": ["color1", "color2"],
            "font_size": 12,
            "line_width": 2,
            "marker_size": 8
        }},
        "layout": {{
            "title": "título",
            "xaxis": {{
                "title": "título eje x",
                "range": [min, max]
            }},
            "yaxis": {{
                "title": "título eje y",
                "range": [min, max]
            }}
        }},
        "annotations": [
            {{
                "text": "texto",
                "x": valor,
                "y": valor,
                "showarrow": true/false
            }}
        ]
    }}
}}
"""

DASHBOARD_LAYOUT_PROMPT = """
Diseña el layout para un dashboard de análisis de mercado.

Datos de entrada:
- Título: {title}
- Componentes: {components}
- Interacciones: {interactions}

Genera una respuesta en formato JSON con la siguiente estructura:
{{
    "layout": {{
        "type": "grid/flow",
        "rows": [
            {{
                "height": "altura",
                "components": [
                    {{
                        "type": "tipo",
                        "width": "ancho",
                        "height": "altura",
                        "position": {{
                            "x": valor,
                            "y": valor
                        }}
                    }}
                ]
            }}
        ],
        "style": {{
            "background_color": "color",
            "padding": "valor",
            "spacing": "valor"
        }},
        "interactions": [
            {{
                "type": "tipo",
                "source": "componente_origen",
                "target": "componente_destino",
                "action": "acción"
            }}
        ]
    }}
}}
"""

ANNOTATION_PROMPT = """
Genera anotaciones para las visualizaciones de mercado.

Datos de entrada:
- Visualización: {visualization}
- Datos: {data}
- Contexto: {context}

Genera una respuesta en formato JSON con la siguiente estructura:
{{
    "annotations": [
        {{
            "text": "texto de la anotación",
            "position": {{
                "x": valor,
                "y": valor
            }},
            "style": {{
                "color": "color",
                "font_size": tamaño,
                "font_weight": "normal/bold"
            }},
            "arrow": {{
                "show": true/false,
                "style": "estilo"
            }}
        }}
    ],
    "highlights": [
        {{
            "type": "tipo",
            "value": "valor",
            "description": "descripción"
        }}
    ],
    "insights": [
        {{
            "text": "texto del insight",
            "importance": "alta/media/baja",
            "related_data": ["dato1", "dato2"]
        }}
    ]
}}
""" 