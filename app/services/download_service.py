import re
import yt_dlp
import logging
import asyncio
from uuid import uuid4
from pathlib import Path
from functools import partial
from typing import List, Optional, Dict, Callable, Coroutine, Any

from app.errors import StorageError
from app.settings import AppSettings
from app.enums import Format, Bitrate
from app.services.lrclib_service import LyricService
from app.services.tag_service import AudioTaggerService
from app.services.cover_service import CoverDownloaderService
from app.schemas import AlbumTrackResponse, AlbumResponse, AudioFile, AudioFilesList

ProgressCallback = Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]

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
        self.lyrics_service: LyricService = LyricService(settings)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.progress_callback: Optional[ProgressCallback] = None
    
    async def _emit_progress(self, current: int, total: int, status: str, track_title: str = ""):
        """
        Envía una actualización de progreso si hay un callback configurado.

        Args:
            current(int): Evento actual
            total (int): Total de eventos
            status (str): Estado actual
            track_title (str, optional): Título de la canción actual. Por defecto es "".
        """
        if self.progress_callback:
            await self.progress_callback({
                "current": current,
                "total": total,
                "percentage": round((current / total) * 100, 2),
                "status": status,
                "track": track_title
            })

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
                    id=uuid4(),
                    file_path=output_path,
                    file_name=track_data.title,
                    file_format=format_ext,
                    file_size=output_path.stat().st_size
                )
            except Exception as e:
                self.logger.error(f"Error descargando {track_data.title} desde {track_data.url_canonical}: {e}")
                return None

    def _download_lyrics(self, track: AlbumTrackResponse, output_path: Path) -> Optional[Path]:
        """
        Descarga y guarda el archivo de letras.
        
        Args:
           track (AlbumTrackResponse): Objeto track generado desde youtube.
           output_path (Path): Ruta de salida para el archivo de letras.
        
        Returns:
           Optional[Path]: Ruta al archivo de letras descargado.
        
        Raises:
            StorageError: Si ocurre un error al crear el archivo de letras.
        """
        # 1. Obtener la letra
        lyrics = self.lyrics_service.get_lyrics_with_fallback(track)
        
        # 2. Si no obtenemos la letra, salimos
        if not lyrics:
            self.logger.warning(f"No se encontraron letras para {track.title}")
            return None
        
        # 3. Creamos el archivo.
        try:
            lrc_path = output_path.with_suffix(".lrc")
            lrc_path.write_text(lyrics, encoding="utf-8")

            if lrc_path.stat().st_size > 0:
                return lrc_path
        except Exception as e:
            self.logger.error(f"Error al crear el archivo de letras: {e}")
            raise StorageError(f"No se pudo crear el archivo de letras: {e}")

    def download_album_to_mp3(
            self, 
            bitrate: Bitrate = Bitrate.B_128K,
            genre: Optional[str] = None
        ) -> AudioFilesList:
        """
        Descarga una lista de pistas de audio desde YouTube en formato mp3.

        Args:
            bitrate (Bitrate, optional): Calidad de audio deseada.
            genre (str, optional): Género musical.

        Returns:
            AudioFilesList: Lista de objetos AudioFile con la información de los archivos descargados.
        """
        tracks: List[AudioFile] = []

        # 1. Descargar el cover
        cover = self.cover_service.download_image(self.album_data.thumbnail, self.album_path / "cover.jpg")
        if cover:
            cover_data = cover.read_bytes()
        
        # 2. Descargar las pistas
        for track in self.album_data.tracks:
            audio_file = self._download_track(track, format_ext=Format.MP3, bitrate=bitrate)
            
            if audio_file:
                self.tag_service.set_mp3_tags(
                    audio_file=audio_file, 
                    track=track, 
                    genre=genre,
                    cover_data=cover_data, 
                )
                
                # 3. Obtenemos el archivo de letras.
                lyrics_path = self._download_lyrics(track, audio_file.file_path)
                
                if lyrics_path:
                    audio_file.lyric_path = lyrics_path
                
                tracks.append(audio_file)
        
        return AudioFilesList(
            count=len(tracks),
            total_size=sum([track.file_size for track in tracks]),
            audio_files=tracks
        )
    
    def download_album_to_m4a(
            self, 
            bitrate: Bitrate = Bitrate.B_128K,
            genre: Optional[str] = None
        ) -> AudioFilesList:
        """
        Descarga una lista de pistas de audio desde YouTube y las guarda en formato m4a.

        Args:
            bitrate (Bitrate, optional): Calidad de audio deseada.
            genre (str, optional): Género musical.
        
        Returns:
            AudioFilesList: Lista de objetos AudioFile con la información de los archivos descargados.
        """
        tracks: List[AudioFile] = []

        # 1. Descargar el cover
        cover = self.cover_service.download_image(self.album_data.thumbnail, self.album_path / "cover.jpg")
        if cover:
            cover_data = cover.read_bytes()
        
        # 2. Descargar las pistas
        for track in self.album_data.tracks:
            audio_file = self._download_track(track, format_ext=Format.M4A, bitrate=bitrate)
            
            if audio_file:
                self.tag_service.set_m4a_tags(
                    audio_file=audio_file, 
                    tags=track, 
                    cover_data=cover_data, 
                    genre=genre
                )
                
                # 3. Obtenemos el archivo de letras.
                lyrics_path = self._download_lyrics(track, audio_file.file_path)
                
                if lyrics_path:
                    audio_file.lyric_path = lyrics_path
                
                tracks.append(audio_file)
        
        return AudioFilesList(
            count=len(tracks),
            total_size=sum([track.file_size for track in tracks]),
            audio_files=tracks
        )   
    
    async def download_album(
        self, 
        format_ext: Format = Format.MP3,
        bitrate: Bitrate = Bitrate.B_128K,
        genre: Optional[str] = None,
        progress_cb: Optional[ProgressCallback] = None
    ) -> AudioFilesList:
        """
        Método unificado para descargar álbumes con soporte de progreso.

        Args:
            format_ext (Format, optional): Formato de audio deseado.
            bitrate (Bitrate, optional): Calidad de audio deseada.
            genre (str, optional): Género musical.
            progress_cb (Optional[ProgressCallback], optional): Callback de progreso.
        
        Returns:
            AudioFilesList: Lista de objetos AudioFile con la información de los archivos descargados.
        """
        self.progress_callback = progress_cb
        tracks: List[AudioFile] = []
        total_tracks = len(self.album_data.tracks)

        # 1. Cover
        await self._emit_progress(0, total_tracks, "Descargando portada...", "Metadata")
        cover = self.cover_service.download_image(self.album_data.thumbnail, self.album_path / "cover.jpg")
        cover_data = cover.read_bytes() if cover else None

        # 2. Bucle de Tracks
        for index, track in enumerate(self.album_data.tracks, 1):
            await self._emit_progress(index - 1, total_tracks, f"Procesando...", track.title)
            
            audio_file = self._download_track(track, format_ext=format_ext, bitrate=bitrate)
            
            if audio_file:
                # Tagging (usando polimorfismo o un if simple según el formato)
                if format_ext == Format.MP3:
                    self.tag_service.set_mp3_tags(audio_file, track, genre, cover_data)
                else:
                    self.tag_service.set_m4a_tags(audio_file, track, cover_data, genre)
                
                # Letras
                lyrics_path = self._download_lyrics(track, audio_file.file_path)
                if lyrics_path:
                    audio_file.lyric_path = lyrics_path
                
                tracks.append(audio_file)
        
        await self._emit_progress(total_tracks, total_tracks, "Completado", "Finalizado")
        
        return AudioFilesList(
            count=len(tracks),
            total_size=sum([t.file_size for t in tracks]),
            audio_files=tracks
        )
    
    async def async_download_album(
        self, 
        format_ext: Format = Format.MP3,
        bitrate: Bitrate = Bitrate.B_128K,
        genre: Optional[str] = None,
        progress_cb: Optional[ProgressCallback] = None
    ) -> AudioFilesList:
        """
        Método unificado optimizado para no bloquear el event loop.

        Args:
            format_ext (Format, optional): Formato de audio deseado.
            bitrate (Bitrate, optional): Calidad de audio deseada.
            genre (str, optional): Género musical.
            progress_cb (Optional[ProgressCallback], optional): Callback de progreso.

        Returns:
            AudioFilesList: Lista de objetos AudioFile con la información de los archivos descargados.
        """
        self.progress_callback = progress_cb
        tracks: List[AudioFile] = []
        total_tracks = len(self.album_data.tracks)
        loop = asyncio.get_running_loop()

        # 1. Cover (operación de red, mejor en executor si es bloqueante)
        await self._emit_progress(0, total_tracks, "Descargando portada...", "Metadata")
        cover = await loop.run_in_executor(None, self.cover_service.download_image, self.album_data.thumbnail, self.album_path / "cover.jpg")
        cover_data = cover.read_bytes() if cover else None

        # 2. Bucle de Tracks
        for index, track in enumerate(self.album_data.tracks, 1):
            # Este emit_progress ahora sí llegará al cliente porque el loop estará libre
            await self._emit_progress(index - 1, total_tracks, f"Descargando...", track.title)
            
            # Ejecutamos la descarga pesada en un hilo separado
            download_func = partial(self._download_track, track, format_ext, bitrate)
            audio_file = await loop.run_in_executor(None, download_func)
            await asyncio.sleep(0.01)
            
            if audio_file:
                # El etiquetado también es bloqueante (I/O de disco), lo ideal es executor
                
                if format_ext == Format.MP3:
                    await self._emit_progress(index - 1, total_tracks, f"Aplicando etiquetas ID3...", track.title)
                    tag_func = partial(self.tag_service.set_mp3_tags, audio_file, track, genre, cover_data)
                    await asyncio.sleep(0.01)
                if format_ext == Format.M4A:
                    await self._emit_progress(index - 1, total_tracks, f"Aplicando etiquetas MP4...", track.title)
                    tag_func = partial(self.tag_service.set_m4a_tags, audio_file, track, genre, cover_data)
                    await asyncio.sleep(0.01)
                
                await loop.run_in_executor(None, tag_func)
                
                # Letras (I/O bloqueante)
                await self._emit_progress(index - 1, total_tracks, f"Buscando letras en LRCLIB...", track.title)
                lyrics_func = partial(self._download_lyrics, track, audio_file.file_path)
                lyrics_path = await loop.run_in_executor(None, lyrics_func)
                await asyncio.sleep(0.01)
                
                if lyrics_path:
                    audio_file.lyric_path = lyrics_path
                    await self._emit_progress(index - 1, total_tracks, f"Letras sincronizadas guardadas.", track.title)
                    await asyncio.sleep(0.01)
                
                tracks.append(audio_file)
        
        await self._emit_progress(total_tracks, total_tracks, "Completado", "Finalizado")
        return AudioFilesList(
            count=len(tracks),
            total_size=sum([t.file_size for t in tracks]),
            audio_files=tracks
        )