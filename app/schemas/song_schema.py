from datetime import datetime, date
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, HttpUrl

from app.enums.response_type import ResponseType

class SongResponse(BaseModel):
    """
    Esquema de respuesta cuando se obtiene información de una canción directo desde su videoId en youtube, sin necesidad de pasar por el endpoint de búsqueda.

    Attributes:
        response_type (ResponseType): El tipo de respuesta (track).
        url_canonical (HttpUrl): La URL canónica de la canción.
        title (str): El título de la canción.
        track_number (int): El número de la canción en el álbum.
        album_name (str): El nombre del álbum.
        artists (List[str]): Los artistas de la canción.
        description (str): La descripción de la canción.
        thumbnail (HttpUrl): La URL de la miniatura de la canción.
        length_seconds (int): La duración de la canción en segundos.
        duration_seconds (int): La duración de la canción en segundos.
        duration_iso (str): La duración de la canción en formato ISO 8601.
        category (str): La categoría de la canción.
        publish_date (date): La fecha de publicación de la canción.
        upload_date (datetime): La fecha y hora de subida de la canción a YouTube.
    """
    response_type: ResponseType = ResponseType.TRACK
    url_canonical: Optional[HttpUrl] = None
    title: str
    track_number: Optional[int] = None
    album_name: Optional[str] = None
    artists: List[str] = []
    description: Optional[str] = None
    thumbnail: Optional[HttpUrl] = None
    length_seconds: int
    duration_seconds: int
    duration_iso: str
    category: str
    publish_date: Optional[datetime] = None
    upload_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)