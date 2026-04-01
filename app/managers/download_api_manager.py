"""
Manager para coordinar las descargas y la comunicación en tiempo real vía WebSockets.
"""
import logging
from uuid import UUID
from typing import Dict, Any, Optional
from fastapi import WebSocket

from app.settings.app_settings import AppSettings
from app.enums import Format, Bitrate
from app.schemas import AlbumResponse
from app.services.download_service import DownloaderService

class DownloadManagerAPI:
    """
    Manager singleton para gestionar conexiones WebSocket y progreso de descargas.
    """

    def __init__(self, settings: AppSettings):
        """
        Inicializa el manager.

        Args:
            settings (AppSettings): Configuración de la aplicación.
        """
        self.settings = settings
        self.active_connections: Dict[UUID, WebSocket] = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    async def register_connection(self, job_id: UUID, websocket: WebSocket) -> None:
        """
        Registra una conexión WebSocket activa.

        Args:
            job_id (UUID): Identificador único del trabajo generado por el cliente.
            websocket (WebSocket): Conexión abierta.
        """
        await websocket.accept()
        self.active_connections[job_id] = websocket
        self.logger.info(f"WebSocket vinculado al job: {job_id}")

    async def _broadcast_progress(self, job_id: UUID, payload: Dict[str, Any]) -> None:
        """
        Envía datos de progreso al socket correspondiente.

        Args:
            job_id (UUID): ID del trabajo.
            payload (Dict[str, Any]): Datos a enviar.
        """
        ws = self.active_connections.get(job_id)
        if ws:
            try:
                await ws.send_json(payload)
            except Exception as e:
                self.logger.error(f"Error enviando progreso al job {job_id}: {e}")
                del self.active_connections[job_id]

    async def download_album_job(
        self,
        job_id: UUID,
        album_data: AlbumResponse,
        format_ext: Format,
        bitrate: Bitrate,
        genre: Optional[str] = None
    ) -> None:
        """
        Ejecuta la descarga e informa el progreso de forma estricta.

        Args:
            job_id (UUID): ID del trabajo.
            album_data (AlbumResponse): Metadata del álbum.
            format_ext (Format): Formato de audio.
            bitrate (Bitrate): Calidad del audio.
            genre (Optional[str]): Género para tags.
        """
        service = DownloaderService(self.settings, album_data)

        # Usamos un lambda o método parcial para el callback de progreso
        async def progress_callback(data: Dict[str, Any]):
            await self._broadcast_progress(job_id, data)

        try:
            await service.async_download_album(
                format_ext=format_ext,
                bitrate=bitrate,
                genre=genre,
                progress_cb=progress_callback
            )
            
            await self._broadcast_progress(job_id, {
                "status": "completed",
                "message": "Proceso finalizado con éxito."
            })
            
        except Exception as e:
            self.logger.error(f"Fallo crítico en job {job_id}: {e}", exc_info=True)
            await self._broadcast_progress(job_id, {
                "status": "error",
                "message": str(e)
            })
        finally:
            # Limpieza opcional de la conexión tras finalizar
            if job_id in self.active_connections:
                await self.active_connections[job_id].close()
                del self.active_connections[job_id]