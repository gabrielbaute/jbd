"""LRC Lib API Client."""
import logging
import requests
from typing import Optional

from app.errors import APIError
from app.settings import AppSettings
from app.schemas import AlbumTrackResponse

class LyricService:
    """
    Cliente para la API de LRCLib.

    Attributes:
        BASE_URL (str): URL base de la API.
    """
    
    BASE_URL: str = "https://lrclib.net/api"

    def __init__(self, settings: AppSettings):
        """
        Inicializa el servicio de de conexión con l API de LRCLib.

        Args:
            settings (AppSettings): Configuración de la aplicación.
        """
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session.timeout = settings.DOWNLOAD_TIMEOUT

    def get_lyrics(self, track: AlbumTrackResponse, synced: bool = True) -> Optional[str]:
        """
        Obtiene la data de la letra sincronizada o plana para un track específico.

        Args:
            track (AlbumTrackResponse): Objeto track generado desde youtube.
            synced (bool): Si la letra debe ser sincronizada o no. Por defecto True.
        
        Returns:
            Optional[str]: Contenido de la letra si se encuentra, None en caso contrario.
        """
        try:
            params = {
                "track_name": track.title,
                "artist_name": track.artists[0],
                "album_name": track.album,
                "duration": int(track.duration_seconds),
            }

            response = self.session.get(
                f"{self.BASE_URL}/get",
                params=params,
                headers={"Accept": "application/json"},
            )

            if response.status_code == 404:
                self.logger.warning(f"Letra no encontrada para: {track.title}")
                return None

            response.raise_for_status()
            data = response.json()

            lyric_type = "syncedLyrics" if synced else "plainLyrics"
            self.logger.info(f"Song lyrics obtained: {lyric_type}")
            return data.get(lyric_type)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al conectar con la API de LRCLib: {str(e)}")
            raise APIError(
                message="Error al conectar con la API de LRCLib.",
                details=str(e),
            )
        except Exception as e:
            self.logger.error(f"Error al obtener las letras: {str(e)}")
            raise APIError(
                message="Error al obtener las letras.",
                details=str(e),
            )
            

    def get_lyrics_with_fallback(self, track: AlbumTrackResponse) -> Optional[str]:
        """
        Intenta obtener la letra de un track sincronizada, si no la encuentra, devuelve la letra en texto plano.

        Args:
            track (AlbumTrackResponse): Objeto track generado desde youtube.

        Returns:
            Optional[str]: Contenido de la letra si se encuentra, None en caso contrario.
        """
        try:
            return self.get_lyrics(track, synced=True) or self.get_lyrics(
                track, synced=False
            )
        except APIError:
            return None