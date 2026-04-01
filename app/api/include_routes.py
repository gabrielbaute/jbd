"""
Helper para cargar todas las rutas de la API.
"""
from fastapi import FastAPI

from app.api.routes.analyze_routes import router as analyze_router
from app.api.routes.download_routes import router as download_router
from app.api.routes.health_routes import router as health_router

def include_routes(app: FastAPI, prefix: str) -> None:
    """
    Incluye todas las rutas de la API en la aplicación FastAPI.

    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.
        prefix (str): Prefijo para las rutas.
    """
    app.include_router(analyze_router, prefix=prefix)
    app.include_router(download_router, prefix=prefix)
    app.include_router(health_router, prefix=prefix)
