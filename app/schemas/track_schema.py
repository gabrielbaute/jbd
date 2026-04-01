from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.enums.response_type import ResponseType

class TrackResponse(BaseModel):
    """
    Modelo de respuesta para un track de una playlist de YouTubeMusic.

    Attributes:
        video_id (str): El ID del video en YouTube.
        title (str): El título de la canción.
        artist (str): El nombre del artista.
        album (str): El nombre del álbum.
        duration (str): La duración de la canción en formato "mm:ss".
        duration_seconds (int): La duración de la canción en segundos.
        thumbnail (str): La URL de la miniatura del video.
    """
    response_type: ResponseType = ResponseType.PLAYLIST_TRACK
    video_id: str
    title: str
    artists: List[str] = []
    album: Optional[str] = None
    duration: str
    duration_seconds: int
    thumbnails: List[str] = []

    model_config = ConfigDict(from_attributes=True)