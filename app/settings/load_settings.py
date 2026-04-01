import sys
from pydantic import ValidationError
from app.settings.app_settings import AppSettings

def load_settings() -> AppSettings:
    """
    Carga la configuración de la aplicación desde variables de entorno.

    Returns:
        AppSettings: Instancia de configuración cargada.

    Raises:
        SystemExit: Si ocurre un error crítico al cargar la configuración.
    """
    try:
        settings = AppSettings()
        settings.ensure_dirs()  # Aseguramos que los directorios existen
        return settings
    except ValidationError as e:
        print(f"ERROR CRÍTICO: Error al cargar la configuración. Detalles: {e}")
        sys.exit(1)

settings = load_settings()