from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.enums.response_type import ResponseType
from app.schemas.track_schema import TrackResponse

class PlaylistResponse(BaseModel):
    """
    Modelo de respuesta para una playlist de YouTubeMusic.

    Attributes:
        response_type (ResponseType): El tipo de respuesta (playlist).
        youtube_id (int): El ID de la playlist en YouTube.
        title (str): El título de la playlist.
        track_count (int): El número de canciones en la playlist.
        duration_seconds (int): La duración total de la playlist en segundos.
    """
    response_type: ResponseType = ResponseType.PLAYLIST
    youtube_id: str
    title: str
    track_count: int
    duration_seconds: int
    tracks: List[TrackResponse] = []

    model_config = ConfigDict(from_attributes=True)