import logging
from typing import  Optional

from app.settings import AppSettings
from app.enums import Format, Bitrate
from app.schemas import AlbumResponse, AudioFilesList
from app.services import YouTubeService, ParserService, DownloaderService

class DownloadManager:
    """
    Clase para gestionar la descarga de listas de audio desde YouTube.
    """
    def __init__(self, settings: AppSettings):
        """
        Inicializa el manager.

        Args:
            settings (AppSettings): Configuración de la aplicación.
        """
        self.settings: AppSettings = settings
        self.youtube_service: YouTubeService = YouTubeService()
        self.logger = logging.getLogger(self.__class__.__name__)

    def download_album(
            self, 
            album_playlist_url: str, 
            genre: Optional[str] = None, 
            bitrate: Optional[Bitrate] = Bitrate.B_128K,
            format: Optional[Format] = Format.MP3
        ) -> AudioFilesList:
        """
        Orquesta la descarga de un album a partir de su link de youtube. El link debe ser tipo playlist.

        Args:
            album_playlist_url (str): URL de la playlist del album
            genre (Optional[str]): Género musical del album.
            bitrate (Optional[Bitrate]): Bitrate de salida de los archivos de audio.
            format (Optional[Format]): Formato de salida de los archivos de audio. Por defecto Mp3.
        
        Returns:
            AudioFilesList: lista y metadata de los archivos generados.
        """
        album_id: str = ParserService.extract_playlist_id(album_playlist_url)
        album_data: AlbumResponse = self.youtube_service.get_tracklist_from_album_playlist_id(album_id)

        download_service = DownloaderService(settings=self.settings, album_data=album_data)
        
        if format == Format.MP3:
            downloads: AudioFilesList = download_service.download_album_to_mp3(
                genre=genre,
                bitrate=bitrate
            )
        
        if format == Format.M4A:
            downloads: AudioFilesList = download_service.download_album_to_m4a(
                genre=genre,
                bitrate=bitrate
            )

        return downloads