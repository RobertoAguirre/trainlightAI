"""Validadores comunes para la aplicación"""
from typing import Dict, Any, List
from .exceptions import ValidationError

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Valida campos requeridos en un diccionario"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Faltan campos requeridos: {', '.join(missing_fields)}")

def validate_numeric_range(value: float, min_value: float, max_value: float) -> None:
    """Valida que un valor numérico esté dentro de un rango"""
    if not min_value <= value <= max_value:
        raise ValidationError(f"El valor {value} está fuera del rango [{min_value}, {max_value}]")

def validate_string_length(value: str, min_length: int, max_length: int) -> None:
    """Valida la longitud de una cadena"""
    if not min_length <= len(value) <= max_length:
        raise ValidationError(
            f"La longitud de la cadena debe estar entre {min_length} y {max_length} caracteres"
        ) 