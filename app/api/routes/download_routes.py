"""
Rutas para la gestión de descargas de álbumes.
"""
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks, WebSocket, WebSocketDisconnect, Depends

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

@router.websocket("/ws/progress/{job_id}")
async def websocket_progress_endpoint(
    websocket: WebSocket,
    job_id: UUID,
    manager: DownloadManagerAPI = Depends(get_download_api_manager)
) -> None:
    """
    Endpoint de WebSocket para el seguimiento en tiempo real del progreso de descarga.

    Args:
        websocket (WebSocket): Instancia de la conexión WebSocket.
        job_id (UUID): Identificador único del trabajo (generado por el frontend).
        manager (DownloadManagerAPI): Manager encargado de la orquestación y sockets.

    Returns:
        None
    """
    # El manager acepta la conexión y la guarda en su diccionario interno
    await manager.register_connection(job_id, websocket)
    
    try:
        while True:
            # Mantenemos la conexión abierta. 
            # El cliente puede enviar pings para evitar timeouts de red.
            await websocket.receive_text()
    except WebSocketDisconnect:
        # La limpieza final del socket la hace el manager en el bloque 'finally'
        # de la tarea en segundo plano (download_album_job).
        pass