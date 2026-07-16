"""
Estructuras de respuesta estandar para la API.
Todas las respuestas exitosas y de error siguen un formato uniforme.
"""

from typing import Any


def success_response(data: Any, message: str | None = None) -> dict[str, Any]:
    """Construye un diccionario de respuesta exitosa."""
    return {"success": True, "data": data, "message": message}


def error_response(
    code: str, message: str, details: dict | list | None = None
) -> dict[str, Any]:
    """Construye un diccionario de respuesta de error."""
    return {
        "success": False,
        "error": {"code": code, "message": message, "details": details},
    }
