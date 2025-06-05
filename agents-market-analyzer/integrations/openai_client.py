import openai
from typing import Dict, Any, Optional

class OpenAIClient:
    """Cliente para interacción con OpenAI API"""
    
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)
    
    async def analyze(self, prompt: str, context: Dict[str, Any], model: str = "gpt-4") -> str:
        """Ejecutar análisis con OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto analista de mercado. Proporciona análisis detallados y basados en datos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error en análisis OpenAI: {str(e)}")
    
    async def generate_structured_analysis(self, prompt: str, context: Dict[str, Any], model: str = "gpt-4") -> Dict[str, Any]:
        """Generar análisis estructurado con formato específico"""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto analista de mercado. Proporciona análisis estructurados en formato JSON."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\nResponde en formato JSON válido."
                    }
                ],
                temperature=0.2,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error en análisis estructurado OpenAI: {str(e)}") 