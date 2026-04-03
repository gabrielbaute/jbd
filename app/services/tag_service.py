import logging
from typing import Optional
from mutagen.id3 import  ID3, APIC, TIT2, TPE1, TPE2, TALB, TDRC, TRCK, TPOS, TCON
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4Tags, MP4, MP4Cover
from mutagen.easyid3 import EasyID3

from app.enums import Format
from app.schemas import AudioFile, AlbumTrackResponse

class AudioTaggerService:
    """
    Servicio para manejar las etiquetas de los archivos de audio.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_mp3_tags(
            self, 
            audio_file: AudioFile, 
            track: AlbumTrackResponse, 
            genre: Optional[str] = None,
            cover_data: Optional[bytes] = None
        ) -> bool:
        """
        Asigna etiquetas a un archivo MP3.

        Args:
            audio_file (AudioFile): Archivo de audio al que se le asignarán las etiquetas.
            track (AlbumTrackResponse): Objeto track generado desde youtube.
            genre (str, optional): Género musical. Por defecto es None.
            cover_data (Optional[bytes], optional): Datos de la portada del álbum. Por defecto es None.

        Returns:
            bool: True si las etiquetas se asignaron correctamente, False en caso contrario.
        """
        if audio_file.file_format != Format.MP3:
            self.logger.error("El archivo no es un MP3.")
            return False
        
        try:
            audio = ID3(audio_file.file_path)
            frames = [
                TIT2(encoding=3, text=track.title),
                TPE1(encoding=3, text=track.artists[0]),
                TPE2(encoding=3, text=track.artists[0]),
                TALB(encoding=3, text=track.album),
                TDRC(encoding=3, text=str(track.publish_date.year)),
                TRCK(encoding=3, text=f"{track.track_number}/{track.total_tracks}")
            ]

            if genre:
                frames.append(TCON(encoding=3, text=genre))

            if cover_data:
                audio.add(
                    APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3,
                        data=cover_data
                    )
                )

            for frame in frames:
                audio.add(frame)

            audio.save(v2_version=3)
            return True
        
        except Exception as e:
            self.logger.error(f"Error setting MP3 tags: {e}")
            return False
    
    def set_m4a_tags(
            self, 
            audio_file: AudioFile, 
            tags: AlbumTrackResponse, 
            genre: Optional[str] = None, 
            cover_data: Optional[bytes] = None
        ) -> bool:
        """
        Asigna etiquetas a un archivo M4A.

        Args:
            audio_file (AudioFile): Archivo de audio al que se le asignarán las etiquetas.
            tags (AlbumTrackResponse): Etiquetas a asignar.
            genre (str, optional): Género musical. Por defecto es None.
            cover_data (Optional[bytes], optional): Datos de la portada del álbum. Por defecto es None.

        Returns:
            bool: True si las etiquetas se asignaron correctamente, False en caso contrario.
        """
        if audio_file.file_format != Format.M4A:
            self.logger.error("El archivo no es un M4A.")
            return False
        
        try:
            audio = MP4(audio_file.file_path)
            if not audio:
                self.logger.error("No se pudo cargar el archivo de audio.")
    
            audio.update({
                '\xa9nam': [tags.title],
                '\xa9ART': ['/'.join(tags.artists)],
                'aART': ['/'.join(tags.artists)],
                '\xa9alb': [tags.album],
                '\xa9day': [str(tags.publish_date.year)],
                'trkn': [(tags.track_number, tags.total_tracks)]
            })

            if genre:
                self.logger.debug(f"Agregando {genre} a {tags.title}")
                audio["\xa9gen"] = genre

            if cover_data:
                self.logger.debug(f"Incorporando el cover art en JPEG a {tags.title}")
                audio['covr'] = [MP4Cover(cover_data)]

            audio.save()
            return True
        
        except Exception as e:
            self.logger.error(f"Error setting M4A tags: {e}")
            return False