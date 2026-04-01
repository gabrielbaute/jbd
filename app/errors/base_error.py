from typing import Any, Dict, Optional

class JBDError(Exception):
    """
    Clase base para manejo de errores legibles para un humano.
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
