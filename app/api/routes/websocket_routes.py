"""
Rutas para la gestión de descargas de álbumes.
"""
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, BackgroundTasks

from app.enums import Format, Bitrate
from app.managers import DownloadManagerAPI
from app.schemas import AlbumResponse, DownloadRequest
from app.api.dependencies import get_download_api_manager

router = APIRouter(prefix="/download", tags=["Download"])

@router.post("/album")
async def start_download(
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
    manager: DownloadManagerAPI = Depends(get_download_api_manager)
):
    """
    Inicia el proceso de descarga en segundo plano y asocia el progreso al job_id.
    """
    # Agregamos la tarea al hilo de ejecución de fondo de FastAPI
    background_tasks.add_task(
        manager.download_album_job,
        job_id=request.job_id,
        album_data=request.album_data,
        format_ext=request.format,
        bitrate=request.bitrate,
        genre=request.genre
    )

    return {
        "status": "accepted",
        "job_id": request.job_id,
        "message": "Descarga enviada a la cola de procesamiento."
    }