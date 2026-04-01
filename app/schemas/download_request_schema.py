from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

from app.enums import Format, Bitrate
from app.schemas.album_response import AlbumResponse

class DownloadRequest(BaseModel):
    """
    Objeto para solicitar la descarga de un álbum filtrado.

    Attributes:
        job_id (UUID): Identificador único de la solicitud de descarga.
        album_data (AlbumResponse): Datos del álbum filtrado. Contiene los tracks ya filtrados/seleccionados por el frontend
        genre (Optional[str]): Género musical para asignar a los tracks del album.
        bitrate (Bitrate): Bitrate para asignar a los tracks del album. Por defecto es B_128K (128kbps).
        format (Format): Formato de descarga de los tracks del album. Por defecto es MP3.
    """
    job_id: UUID
    album_data: AlbumResponse
    format: Format = Format.MP3
    bitrate: Bitrate = Bitrate.B_128K
    genre: Optional[str] = None    