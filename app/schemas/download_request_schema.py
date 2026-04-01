from pydantic import BaseModel
from typing import List, Optional

from app.enums import Format, Bitrate
from app.schemas import AlbumResponse

class DownloadRequest(BaseModel):
    """
    Objeto para solicitar la descarga de un álbum filtrado.

    Attributes:
        album_data (AlbumResponse): Datos del álbum filtrado. Contiene los tracks ya filtrados/seleccionados por el frontend
        genre (Optional[str]): Género musical para asignar a los tracks del album.
        bitrate (Bitrate): Bitrate para asignar a los tracks del album. Por defecto es B_128K (128kbps).
        format (Format): Formato de descarga de los tracks del album. Por defecto es MP3.
    """
    album_data: AlbumResponse
    genre: Optional[str] = None
    bitrate: Bitrate = Bitrate.B_128K
    format: Format = Format.MP3