import anthropic
from typing import Dict, Any

class AnthropicClient:
    """Cliente para interacción con Anthropic API"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
    
    async def analyze(self, prompt: str, context: Dict[str, Any], model: str = "claude-3-sonnet-20240229") -> str:
        """Ejecutar análisis con Anthropic"""
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=6000,
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Error en análisis Anthropic: {str(e)}")
    
    async def generate_structured_analysis(self, prompt: str, context: Dict[str, Any], model: str = "claude-3-sonnet-20240229") -> Dict[str, Any]:
        """Generar análisis estructurado con formato específico"""
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=6000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\nResponde en formato JSON válido."
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Error en análisis estructurado Anthropic: {str(e)}") 