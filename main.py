""" 
Entrypoint de la API
"""
import uvicorn

from app.api.app_factory import create_app
from app.api.error_handler import register_error_handlers

from app.settings.load_settings import settings
from app.settings.app_logs import JBDLogger

# Configuración de logger
JBDLogger.setup_logging(level="INFO")

# Creación de la aplicación
app = create_app(settings=settings)

# Handler de errores
register_error_handlers(app)

def run_server():
    """
    Lanza el servidor de uvicorn
    """
    uvicorn.run(
        app=app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.API_LOG_LEVEL,
        reload=settings.API_RELOAD,
    )

if __name__ == "__main__":
    run_server()