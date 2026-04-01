import sys
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_settings
from app.settings.app_settings import AppSettings

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/")
async def get_current_settings(settings: AppSettings = Depends(get_settings)):
    """
    Retorna la configuración actual procesada por la aplicación.
    
    Args:
        settings (AppSettings): Instancia única de configuración.
        
    Returns:
        dict: Diccionario con los valores actuales de configuración.
    """
    # Excluimos campos internos o excesivamente técnicos para la UI
    exclude_set = {
        "BASE_PATH", 
        "STATIC_PATH", 
        "TMP_PATH", 
        "INSTANCE_PATH", 
        "LOGS_PATH"
    }
    return settings.model_dump(exclude=exclude_set)

@router.post("/")
async def update_settings(
    new_data: Dict[str, str], 
    settings: AppSettings = Depends(get_settings)
):
    """
    Actualiza el archivo .env persistente con los nuevos valores proporcionados.
    
    Args:
        new_data (Dict[str, str]): Diccionario con las llaves y valores a modificar.
        settings (AppSettings): Instancia única de configuración.
        
    Returns:
        dict: Mensaje de confirmación.
        
    Raises:
        HTTPException: Si ocurre un error al escribir el archivo.
    """
    try:
        # 1. Actualizamos temporalmente el objeto en memoria para reflejar los cambios en el dump
        # Esto permite que el template recoja los valores actualizados
        for key, value in new_data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        # 2. Re-generamos el contenido del .env con el formato seguro (texto plano)
        # Usamos el mismo diseño que en el bootstrap para mantener consistencia
        env_content = f"""# JBD PERSISTENT CONFIGURATION
# Versión: {settings.APP_VERSION}
# Last Updated via API

# --- GENERAL ---
APP_NAME={settings.APP_NAME}
DOWNLOAD_TIMEOUT={settings.DOWNLOAD_TIMEOUT}

# --- DIRECTORIOS ---
DATA_PATH={settings.DATA_PATH}
YTDLP_COOKIES_PATH={settings.YTDLP_COOKIES_PATH}

# --- API & SERVER ---
API_HOST={settings.API_HOST}
API_PORT={settings.API_PORT}
API_RELOAD={settings.API_RELOAD}
API_LOG_LEVEL={settings.API_LOG_LEVEL}
APP_URL={settings.APP_URL}
"""

        # 3. Sobrescribimos el archivo físico
        with open(settings.USER_ENV_FILE, "w", encoding="utf-8") as f:
            f.write(env_content)

        return {
            "status": "success",
            "message": "Configuración guardada en .env. Reinicie el servicio para aplicar los cambios globales."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al actualizar la configuración: {str(e)}"
        )