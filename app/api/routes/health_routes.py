"""
Módulo para las rutas de check health y status
"""
from fastapi import APIRouter,  status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/check", tags=["Check-Health"])

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint para verificar que la API está funcionando.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "OK",
            "message": "API is running flawlessly",
        }
    )