from app.errors.base_error import JBDError

class APIError(JBDError):
    """Error de comunicación con una API externa."""
    pass

class ValidationError(JBDError):
    """Error de validación de datos o reglas de negocio."""
    pass

class ResourceNotFoundError(JBDError):
    """Cuando un recurso (User, Photo, Album) no existe."""
    pass

class StorageError(JBDError):
    """Errores físicos de disco o cuota."""
    pass

class PermissionDeniedError(JBDError):
    """Cuando un usuario no tiene permisos para realizar una acción."""
    pass