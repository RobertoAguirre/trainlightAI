# Analizador de Mercado

Sistema de análisis de mercado basado en agentes inteligentes.

## 🚀 Características

- Análisis primario de mercado con OpenAI GPT-4
- Análisis secundario profundo con Anthropic Claude
- Generación de reportes en PDF
- Integración con chatbot-ingestor-core
- Sistema de validación en tiempo real
- Orquestación automática de agentes

## 📋 Requisitos

- Python 3.8+
- Docker (opcional)
- API Keys de OpenAI y Anthropic

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/agents-market-analyzer.git
cd agents-market-analyzer
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## ⚙️ Configuración

Crear archivo `.env` con las siguientes variables:

```env
OPENAI_API_KEY=tu-api-key-de-openai
ANTHROPIC_API_KEY=tu-api-key-de-anthropic
CORE_API_URL=http://localhost:8000
```

## 🚀 Uso

1. Ejecutar la aplicación:
```bash
python main.py
```

2. Ejecutar con Docker:
```bash
docker-compose up
```

## 🧪 Testing

```bash
python -m pytest
```

## 📝 Estructura del Proyecto

```
agents-market-analyzer/
├── agents/                 # Agentes de análisis
├── configs/               # Configuraciones
├── integrations/          # Integraciones externas
├── utils/                 # Utilidades
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias
└── docker-compose.yml    # Configuración Docker
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Componentes Principales

- `MarketAnalyzerAgent`: Análisis de mercado
- `MarketPredictorAgent`: Predicciones de mercado
- `MarketVisualizerAgent`: Visualizaciones
- `MarketIntegratorAgent`: Integración de resultados
- `MarketOrchestratorAgent`: Orquestación del flujo

## Configuración

Las configuraciones principales se encuentran en:
- `configs/app_config.py`: Configuración general
- `configs/logging_config.py`: Configuración de logs 