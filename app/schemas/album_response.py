from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, HttpUrl

from app.enums.response_type import ResponseType

class AlbumTrackResponse(BaseModel):
    """
    Modelo de respuesta para los detalles de una canción extraída desde el link de un álbum.

    Attributes:
        response_type (ResponseType): El tipo de respuesta (album_track).
        video_id (str): El ID del video en YouTube.
        title (str): El título de la canción.
        artists (List[str]): Los artistas de la canción.
        album (str): El nombre del álbum.
        track_number (int): El número de la canción en el álbum.
        url_canonical (HttpUrl): La URL canónica de la canción.
        thumbnail (HttpUrl): La URL de la miniatura de la canción.
        length_seconds (int): La duración de la canción en segundos.
        duration_seconds (int): La duración de la canción en segundos.
        duration_iso (str): La duración de la canción en formato ISO 8601.
        category (str): La categoría de la canción.
        publish_date (date): La fecha de publicación de la canción.
        upload_date (datetime): La fecha y hora de subida de la canción a YouTube.
        year (int): El año de lanzamiento del álbum.
        total_tracks (int): El número total de canciones en el álbum.
    """
    response_type: ResponseType = ResponseType.ALBUM_TRACK
    video_id: str
    title: str
    artists: List[str] = []
    album: Optional[str] = None
    track_number: Optional[int] = None

    # Datos de segundo procesamiento
    url_canonical: Optional[HttpUrl] = None
    thumbnail: Optional[HttpUrl] = None
    length_seconds: Optional[int] = None
    duration_seconds: Optional[int] = None
    duration_iso: Optional[str] = None
    category: Optional[str] = None
    publish_date: Optional[datetime] = None
    upload_date: Optional[datetime] = None
    year: Optional[int] = None
    total_tracks: Optional[int] = None
    
    model_config = ConfigDict(extra="forbid")

class AlbumResponse(BaseModel):
    """
    Modelo de respuesta para los detalles de un álbum.

    Attributes:
        response_type (ResponseType): El tipo de respuesta (album).
        title (str): El título del álbum.
        youtube_type (str): El tipo de contenido en YouTube (por ejemplo, "album").
        is_explicit (bool): Indica si el álbum es explícito.
        description (str): La descripción del álbum.
        year (int): El año de lanzamiento del álbum.
        artists (List[str]): Los artistas del álbum.
        track_count (int): El número de canciones en el álbum.
        thumbnail (HttpUrl): La URL de la miniatura del álbum.
        tracks (List[AlbumTrackResponse]): Los detalles de las canciones del álbum.
    """
    response_type: ResponseType = ResponseType.ALBUM
    title: Optional[str] = None
    youtube_type: Optional[str] = None
    is_explicit: Optional[bool] = None
    description: Optional[str] = None
    year: int
    artists: List[str] = []
    track_count: int
    thumbnail: Optional[HttpUrl] = None
    tracks: List[AlbumTrackResponse] = []
    
    model_config = ConfigDict(extra="forbid")

