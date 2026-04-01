import sys
from pydantic import ValidationError
from app.settings.app_settings import AppSettings

def load_settings() -> AppSettings:
    """
    Carga la configuración de la aplicación y asegura el entorno de ejecución.

    Returns:
        AppSettings: Instancia única de configuración cargada y validada.

    Raises:
        SystemExit: Si la validación de Pydantic falla o hay errores de permisos.
    """
    try:
        # 1. Instanciamos (Pydantic lee los .env definidos en model_config)
        settings = AppSettings()
        
        # 2. Ejecutamos bootstrap (Crea directorios y genera el .env persistente si no existe)
        # Este método ya incluye internamente la llamada a ensure_dirs()
        settings.bootstrap()
        
        return settings
    except ValidationError as e:
        print(f"ERROR CRÍTICO: Error al cargar la configuración. Detalles: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR CRÍTICO: Fallo inesperado durante el bootstrap: {e}")
        sys.exit(1)

# Instancia Singleton compartida en toda la aplicación
settings = load_settings()