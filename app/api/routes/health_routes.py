"""
Módulo para las rutas de check health y status
"""
from fastapi import APIRouter,  status, Depends
from fastapi.responses import JSONResponse

from app.api.dependencies import get_settings
from app.settings.app_settings import AppSettings

router = APIRouter(prefix="/check", tags=["Check-Health"])

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(settings: AppSettings = Depends(get_settings)):
    """
    Health check endpoint para verificar que la API está funcionando.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "OK",
            "message": "API is running flawlessly",
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION
        }
    )