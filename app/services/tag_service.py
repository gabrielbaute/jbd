import logging
from typing import Optional
from mutagen.id3 import  ID3, APIC, TIT2, TPE1, TPE2, TALB, TDRC, TRCK, TCON
from mutagen.mp4 import MP4Tags, MP4, MP4Cover
from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
from mutagen.oggopus import OggOpus
from mutagen.flac import Picture
from mutagen.aac import AAC

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
                audio["\xa9gen"] = [genre]

            if cover_data:
                self.logger.debug(f"Incorporando el cover art en JPEG a {tags.title}")
                audio['covr'] = [MP4Cover(cover_data)]

            audio.save()
            return True
        
        except Exception as e:
            self.logger.error(f"Error setting M4A tags: {e}")
            return False

    def set_ogg_tags(
            self, 
            audio_file: AudioFile, 
            track: AlbumTrackResponse, 
            genre: Optional[str] = None,
            cover_data: Optional[bytes] = None
        ) -> bool:
        """
        Asigna etiquetas Vorbis Comment a un archivo OGG.

        Args:
            audio_file (AudioFile): Archivo de audio al que se le asignarán las etiquetas.
            track (AlbumTrackResponse): Objeto track con la metadata.
            genre (str, optional): Género musical.
            cover_data (Optional[bytes], optional): Datos de la portada.

        Returns:
            bool: True si tuvo éxito, False en caso contrario.
        """
        if audio_file.file_format != Format.OGG:
            self.logger.error("El archivo no es un OGG.")
            return False

        try:
            audio = OggVorbis(audio_file.file_path)
            
            # Las etiquetas Vorbis son simples mapeos de texto
            audio["title"] = track.title
            audio["artist"] = track.artists
            audio["album"] = track.album
            audio["date"] = str(track.publish_date.year)
            audio["tracknumber"] = str(track.track_number)
            audio["totaltracks"] = str(track.total_tracks)

            if genre:
                audio["genre"] = genre

            if cover_data:
                # OGG utiliza el estándar de metadata FLAC para imágenes
                picture = Picture()
                picture.data = cover_data
                picture.type = 3  # Front Cover
                picture.mime = "image/jpeg"
                
                # Se codifica en base64 internamente mediante el campo metadata_block_picture
                import base64
                picture_data = picture.write()
                encoded_data = base64.b64encode(picture_data).decode("ascii")
                audio["metadata_block_picture"] = [encoded_data]

            audio.save()
            return True
        except Exception as e:
            self.logger.error(f"Error setting OGG tags: {e}")
            return False

    def set_opus_tags(
            self, 
            audio_file: AudioFile, 
            track: AlbumTrackResponse, 
            genre: Optional[str] = None,
            cover_data: Optional[bytes] = None
        ) -> bool:
        """
        Asigna etiquetas a un archivo Opus (formato Vorbis Comment).

        Args:
            audio_file (AudioFile): Archivo de audio .opus.
            track (AlbumTrackResponse): Metadata del track.
            genre (str, optional): Género musical.
            cover_data (Optional[bytes], optional): Datos de la portada.

        Returns:
            bool: True si tuvo éxito, False en caso contrario.
        """
        if audio_file.file_format != Format.OPUS:
            self.logger.error("El archivo no es un Opus.")
            return False

        try:
            # OggOpus hereda casi toda la lógica de Vorbis
            audio = OggOpus(audio_file.file_path)
            
            audio["title"] = track.title
            audio["artist"] = track.artists
            audio["album"] = track.album
            audio["date"] = str(track.publish_date.year)
            audio["tracknumber"] = str(track.track_number)

            if genre:
                audio["genre"] = genre

            if cover_data:
                picture = Picture()
                picture.data = cover_data
                picture.type = 3
                picture.mime = "image/jpeg"
                
                picture_data = picture.write()
                import base64
                encoded_data = base64.b64encode(picture_data).decode("ascii")
                audio["metadata_block_picture"] = [encoded_data]

            audio.save()
            return True
        except Exception as e:
            self.logger.error(f"Error setting Opus tags: {e}")
            return False

    def set_aac_tags(
            self, 
            audio_file: AudioFile, 
            track: AlbumTrackResponse, 
            genre: Optional[str] = None
        ) -> bool:
        """
        Asigna etiquetas a un archivo AAC raw. 
        Nota: AAC raw tiene soporte limitado; se recomienda usar contenedores M4A.

        Args:
            audio_file (AudioFile): Archivo .aac.
            track (AlbumTrackResponse): Metadata.
            genre (str, optional): Género musical.

        Returns:
            bool: True si se logró asignar (vía ID3 si el archivo lo permite).
        """
        try:
            # Muchos archivos AAC aceptan etiquetas ID3 al inicio o final
            # Intentamos usar EasyID3 que es una interfaz simplificada
            try:
                audio = EasyID3(audio_file.file_path)
            except:
                # Si no tiene cabecera ID3, la creamos
                tags = ID3()
                tags.save(audio_file.file_path)
                audio = EasyID3(audio_file.file_path)

            audio["title"] = track.title
            audio["artist"] = track.artists[0]
            audio["album"] = track.album
            audio["date"] = str(track.publish_date.year)
            audio["tracknumber"] = f"{track.track_number}/{track.total_tracks}"

            if genre:
                audio["genre"] = genre

            audio.save()
            return True
        except Exception as e:
            self.logger.error(f"Error setting AAC tags: {e}")
            return False