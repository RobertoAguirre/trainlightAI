from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ValidationResult(BaseModel):
    """Resultado de una validación"""
    is_valid: bool
    message: str
    suggestions: List[str] = []

class ValidationEngine:
    """Validación en tiempo real con feedback contextual"""
    
    def __init__(self):
        self.field_rules: Dict[str, Dict[str, Any]] = {}
        self.structure_rules: Dict[str, List[str]] = {}
    
    async def validate_field(self, field: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """Validar campo individual con contexto"""
        if field not in self.field_rules:
            return ValidationResult(
                is_valid=True,
                message="No hay reglas de validación para este campo"
            )
        
        rules = self.field_rules[field]
        errors = []
        suggestions = []
        
        # Validación básica de tipo
        if "type" in rules and not isinstance(value, rules["type"]):
            errors.append(f"El campo debe ser de tipo {rules['type'].__name__}")
        
        # Validación de longitud para strings
        if isinstance(value, str):
            if "min_length" in rules and len(value) < rules["min_length"]:
                errors.append(f"El texto debe tener al menos {rules['min_length']} caracteres")
            if "max_length" in rules and len(value) > rules["max_length"]:
                errors.append(f"El texto no debe exceder {rules['max_length']} caracteres")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            message=", ".join(errors) if errors else "Campo válido",
            suggestions=suggestions
        )
    
    async def validate_structure(self, context: Dict[str, Any], target_step: str) -> ValidationResult:
        """Validar completitud para avanzar de paso"""
        if target_step not in self.structure_rules:
            return ValidationResult(
                is_valid=True,
                message="No hay reglas de estructura para este paso"
            )
        
        required_fields = self.structure_rules[target_step]
        missing_fields = [field for field in required_fields if field not in context.get("data", {})]
        
        return ValidationResult(
            is_valid=len(missing_fields) == 0,
            message=f"Faltan campos requeridos: {', '.join(missing_fields)}" if missing_fields else "Estructura válida",
            suggestions=[f"Por favor, proporciona el campo: {field}" for field in missing_fields]
        )
    
    async def suggest_next_action(self, context: Dict[str, Any]) -> str:
        """Sugerir al usuario qué hacer siguiente"""
        # Implementación básica - se puede mejorar con lógica más sofisticada
        data = context.get("data", {})
        for step, required_fields in self.structure_rules.items():
            missing = [field for field in required_fields if field not in data]
            if missing:
                return f"Por favor, proporciona información sobre: {', '.join(missing)}"
        
        return "Todos los campos requeridos han sido completados" 