"""Configuraciones para los agentes de Market Analyzer"""

AGENT_CONFIGS = {
    "primary_analysis": {
        "ai_provider": "openai",
        "model": "gpt-4",
        "max_tokens": 4000,
        "temperature": 0.3,
        "required_fields": ["company_name", "product_description", "target_market"],
        "trigger_condition": {
            "completion_threshold": 0.8,
            "required_fields_present": True
        },
        "endpoint": "http://localhost:8001/agents/primary_analysis/execute"
    },
    "secondary_analysis": {
        "ai_provider": "anthropic", 
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 6000,
        "temperature": 0.2,
        "required_results": ["primary_analysis"],
        "trigger_condition": {
            "depends_on": ["primary_analysis"],
            "primary_analysis_complete": True
        },
        "endpoint": "http://localhost:8001/agents/secondary_analysis/execute"
    },
    "report_generator": {
        "ai_provider": "openai",
        "model": "gpt-4",
        "max_tokens": 8000,
        "temperature": 0.1,
        "required_results": ["primary_analysis", "secondary_analysis"],
        "trigger_condition": {
            "depends_on": ["primary_analysis", "secondary_analysis"],
            "all_analyses_complete": True
        },
        "endpoint": "http://localhost:8001/agents/report_generator/execute"
    }
} 