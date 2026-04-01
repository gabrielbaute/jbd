"""
Módulo de dependencias para la inyección en las rutas de FastAPI.
"""
from fastapi import Depends
from typing import Optional

from app.settings.load_settings import settings
from app.settings.app_settings import AppSettings
from app.services.youtube_service import YouTubeService
from app.managers import DownloadManager, DownloadManagerAPI

_download_api_manager_instance: Optional[DownloadManagerAPI] = None

def get_settings() -> AppSettings:
    """
    Provee la instancia única de configuración.
    
    Returns:
        AppSettings: Configuración de la aplicación.
    """
    return settings

def get_youtube_service() -> YouTubeService:
    """
    Provee una instancia del servicio de YouTube.
    
    Returns:
        YouTubeService: Instancia del servicio.
    """
    return YouTubeService()

def get_download_manager(
    settings: AppSettings = Depends(get_settings)
) -> DownloadManager:
    """
    Provee la instancia del gestor de descargas.
    
    Args:
        settings (AppSettings): Configuración inyectada.
        
    Returns:
        DownloadManager: Instancia del manager configurada.
    """
    return DownloadManager(settings)

def get_download_api_manager(
    settings: AppSettings = Depends(get_settings)
) -> DownloadManagerAPI:
    """
    Provee la instancia única del gestor de descargas por sockets.
    """
    global _download_api_manager_instance
    if _download_api_manager_instance is None:
        _download_api_manager_instance = DownloadManagerAPI(settings)
    return _download_api_manager_instance