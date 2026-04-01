"""
Rutas para la gestión de descargas de álbumes.
"""
import shutil
import tempfile
from uuid import UUID
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import FileResponse

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

@router.get("/album/zip/{job_id}")
async def download_album_zip(
    job_id: UUID,
    manager: DownloadManagerAPI = Depends(get_download_api_manager)
):
    """
    Busca el resultado de un job finalizado, comprime los archivos y los sirve.
    """
    # 1. Verificar si el job existe y terminó
    result = manager.results.get(job_id)
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="El archivo no existe o el proceso no ha finalizado."
        )

    # 2. Obtener la carpeta donde están los archivos (usando el path del primer archivo)
    if not result.audio_files:
         raise HTTPException(status_code=404, detail="No hay archivos para comprimir.")
    
    album_dir = result.audio_files[0].file_path.parent
    zip_filename = f"{album_dir.name}.zip"
    
    # Creamos un path para el ZIP (por ejemplo en la carpeta temporal del sistema)
    temp_zip_path = Path(tempfile.gettempdir()) / f"{job_id}.zip"

    # 3. Comprimir (Operación bloqueante, idealmente en executor pero aquí simplificado)
    # zip_name sin extensión porque make_archive la añade
    shutil.make_archive(str(temp_zip_path.with_suffix('')), 'zip', album_dir)

    # 4. Retornar el archivo y limpiar el resultado del manager para liberar memoria
    # Nota: podrías borrar manager.results[job_id] aquí o con un BackgroundTask
    return FileResponse(
        path=temp_zip_path,
        filename=zip_filename,
        media_type='application/zip'
    )