"""
Módulo para crear y configurar la aplicación FastAPI (app factory).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings.app_settings import AppSettings
from app.api.include_routes import include_routes
from app.api.web_client import setup_web_client

def create_app(settings: AppSettings) -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    
    Args:
        settings (Settings): Las configuraciones de la aplicación.
    
    Returns:
        FastAPI: Instancia de la aplicación FastAPI configurada.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=f"{settings.APP_NAME} API",
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.API_ALLOW_ORIGINS,
        allow_credentials=settings.API_ALLOW_CREDENTIALS,
        allow_methods=settings.API_ALLOW_METHODS,
        allow_headers=settings.API_ALLOW_HEADERS,
    )

    # Router
    include_routes(app, prefix="/api/v1")

    # Cliente web
    setup_web_client(app, settings)

    return app