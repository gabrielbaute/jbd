import re
import logging
import yt_dlp
from pathlib import Path
from typing import List, Optional, Dict

from app.enums import Format, Bitrate
from app.settings import AppSettings
from app.services.tag_service import AudioTaggerService
from app.services.cover_service import CoverDownloaderService
from app.schemas import AlbumTrackResponse, AlbumResponse, AudioFile, AudioFilesList

class DownloaderService:
    """
    Clase para gestionar la descarga de listas de audio desde YouTube.
    """

    def __init__(self, settings: AppSettings, album_data: AlbumResponse):
        """Inicializa el descargador con la ruta de salida.

        Args:
            settings (AppSettings): Configuración de la aplicación.
            album_data (AlbumResponse): Información del álbum obtenida desde YoutubeService.
        """
        self.cookies_path = settings.YTDLP_COOKIES_PATH
        self.album_data = album_data
        self.temp_dir: Path = settings.TMP_PATH
        self.output_path: Path = settings.DATA_PATH
        self.album_path: Path = self._build_album_path()
        self.cover_service: CoverDownloaderService = CoverDownloaderService(settings)
        self.tag_service: AudioTaggerService = AudioTaggerService()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitiza el nombre del archivo para que sea seguro en Windows, reemplazando caracteres problemáticos y limitando la longitud.

        Args:
            filename: nombre del archivo a sanitizar

        Returns:
            str: nombre del archivo sanitizado seguro para Windows
        """
        # Reemplaza caracteres no permitidos en Windows con guiones bajos
        filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

        # Reemplaza guiones largos por guiones normales
        filename = filename.replace("–", "-").replace("—", "-")

        # Reemplaza múltiples espacios por un solo espacio
        filename = re.sub(r"\s+", " ", filename)

        # Elimina espacios y puntos al principio y al final del nombre del archivo
        filename = filename.strip(". ")

        # Limita la longitud del nombre del archivo a 200 caracteres para evitar problemas con rutas largas en Windows
        if len(filename) > 200:
            filename = filename[:200].strip()

        return filename

    def _build_album_path(self) -> Path:
        """Construye la ruta de salida para un álbum específico.

        Args:
            album (AlbumResponse): Información del álbum.

        Returns:
            Path: Ruta de salida para el álbum.
        """
        artist_name = self._sanitize_filename(self.album_data.artists[0] if self.album_data.artists else "Unknown Artist")
        album_name = self._sanitize_filename(self.album_data.title if self.album_data.title else "Unknown Album")
        year = self.album_data.year

        album_path = self.output_path / artist_name / f"{album_name} ({year})"
        album_path.mkdir(parents=True, exist_ok=True)
        
        return album_path


    def _build_output_path(self, track: AlbumTrackResponse, format_ext: Format = Format.MP3) -> Path:
        """Construye la ruta de salida para un álbum específico.

        Args:
            track (AlbumTrackResponse): Información del álbum.
            format_ext (Format): Formato de audio deseado.

        Returns:
            Path: Ruta de salida para el álbum y el track.
        """
        artist_name = self._sanitize_filename(track.artists[0] if track.artists else "Unknown Artist")
        track_name = self._sanitize_filename(track.title if track.title else "Unknown Track")
        
        return self.album_path / f"{track.track_number} - {artist_name} - {track_name}.{format_ext.value}"
    
    def _configure_ydl_opts(
            self, 
            output_path: Optional[Path],
            format_ext: Format = Format.MP3,
            bitrate: Bitrate = Bitrate.B_128K
        ) -> Dict[str, any]:
        """
        Configura las opciones para yt-dlp.

        Args:
            output_path (Optional[Path]): Ruta de salida para el archivo.
            format_ext (Format): Formato de audio deseado.
            bitrate (Bitrate): Calidad de audio deseada.

        Returns:
            Dict[str, any]: Diccionario de opciones para yt-dlp.
        """
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_path.with_suffix(f".%(ext)s")),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_ext.value,
                'preferredquality': str(bitrate.value),
            }],
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True,
            "cookiefile": self.cookies_path,
        }
        return self.ydl_opts
    
    def _download_track(
            self, 
            track_data: AlbumTrackResponse,
            format_ext: Format = Format.MP3,
            bitrate: Bitrate = Bitrate.B_128K,
        ) -> Optional[AudioFile]:
        """Descarga una pista de audio desde YouTube.

        Args:
            url (str): URL de la pista en YouTube.
            track_name (str): Nombre de la pista.
            album_name (str): Nombre del álbum.
            artist_name (str): Nombre del artista.
            format_ext (Format, optional): Formato de audio deseado. Por defecto es MP3.
            bitrate (Bitrate, optional): Calidad de audio deseada. Por defecto es 128K.

        Returns:
            AudioFile: Objeto AudioFile con la información del archivo descargado.
        """
        output_path = self._build_output_path(track=track_data, format_ext=format_ext)
        self.logger.info(f"Descargando: {track_data.title} desde {track_data.url_canonical} a {output_path}")
       
        ydl_opts = self._configure_ydl_opts(output_path, format_ext, bitrate)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download(str(track_data.url_canonical))
                self.logger.info(f"Descarga completada: {track_data.title}")
                return AudioFile(
                    file_path=output_path,
                    file_name=track_data.title,
                    file_format=format_ext,
                    file_size=output_path.stat().st_size
                )
            except Exception as e:
                self.logger.error(f"Error descargando {track_data.title} desde {track_data.url_canonical}: {e}")
                return None
            
    def download_album_to_mp3(
            self, 
            bitrate: Bitrate = Bitrate.B_128K,
            genre: Optional[str] = None
        ) -> AudioFilesList:
        """
        Descarga una lista de pistas de audio desde YouTube.

        Args:
            bitrate (Bitrate, optional): Calidad de audio deseada.
            genre (str, optional): Género musical.

        Returns:
            AudioFilesList: Lista de objetos AudioFile con la información de los archivos descargados.
        """
        tracks: List[AudioFile] = []
        cover = self.cover_service.download_image(self.album_data.thumbnail, self.album_path / "cover.jpg")
        if cover:
            cover_data = cover.read_bytes()
        
        for track in self.album_data.tracks:
            audio_file = self._download_track(track, format_ext=Format.MP3, bitrate=bitrate)
            
            if audio_file:
                self.tag_service.set_mp3_tags(audio_file, track, cover_data=cover_data, genre=genre)
            
            if audio_file:
                tracks.append(audio_file)
        
        return AudioFilesList(
            count=len(tracks),
            total_size=sum([track.file_size for track in tracks]),
            audio_files=tracks
        )