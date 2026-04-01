import logging
from typing import List, Optional
from ytmusicapi import YTMusic

from app.enums.response_type import ResponseType
from app.schemas import SongResponse, TrackResponse, PlaylistResponse, AlbumResponse, AlbumTrackResponse

class YouTubeService:
    """
    Servicio para interactuar con la API de YouTube Music.
    """

    def __init__(self):
        self.ytmusic = YTMusic()
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_song(self, video_id: str) -> Optional[SongResponse]:
        """
        Obtiene los detalles de una canción a partir de su ID de video.

        Args:
            video_id (str): El ID del video de YouTube.

        Returns:
            Optional[SongResponse]: Los detalles de la canción o None en caso de error.
        """
        try:
            song = self.ytmusic.get_song(video_id)
            mc = song.get("microformat", {})
            microformat = mc.get("microformatDataRenderer", {})
            video_details = song.get("videoDetails", {})
            thumbnails = video_details.get("thumbnail", {}).get("thumbnails", [])

            return SongResponse(
                response_type=ResponseType.TRACK,
                url_canonical=microformat.get("urlCanonical"),
                title=video_details.get("title"),
                description=video_details.get("description"),
                thumbnail=thumbnails[-1].get("url") if thumbnails else None,
                length_seconds=video_details.get("lengthSeconds"),
                duration_seconds=microformat.get("videoDetails", {}).get("durationSeconds"),
                duration_iso=str(microformat.get("videoDetails", {}).get("durationIso8601")),
                category=microformat.get("category"),
                publish_date=microformat.get("publishDate"),
                upload_date=microformat.get("uploadDate")
            )
        except Exception as e:
            self.logger.error(f"Error al obtener la canción con ID {video_id}: {e}")
            return None
        
    def get_tracklist_from_playlist(self, playlist_id: str) -> Optional[PlaylistResponse]:
        """
        Obtiene la lista de canciones de una playlist a partir de su ID.

        Args:
            playlist_id (str): El ID de la playlist de YouTube.

        Returns:
            Optional[PlaylistResponse]: Los detalles de la playlist y su lista de canciones o None en caso de error.
        """
        try:
            playlist = self.ytmusic.get_playlist(playlist_id)
            tracks = playlist.get("tracks", [])

            return PlaylistResponse(
                youtube_id=playlist.get("id"),
                title=playlist.get("title"),
                track_count=playlist.get("trackCount"),
                duration_seconds=playlist.get("duration_seconds"),
                tracks=[
                    TrackResponse(
                        response_type=ResponseType.PLAYLIST_TRACK,
                        video_id=track.get("videoId"),
                        title=track.get("title"),
                        artists=[artist.get("name") for artist in track.get("artists", [])],
                        album=track.get("album", {}).get("name"),
                        duration=track.get("duration"),
                        duration_seconds=track.get("duration_seconds"),
                        thumbnails=[thumbnail.get("url") for thumbnail in track.get("thumbnails", [])],
                    )
                    for track in tracks
                ],
            )
        except Exception as e:
            self.logger.error(f"Error al obtener la playlist desde el ID {playlist_id}: {e}")
            return None

    def process_track(self, track: dict, total_tracks: int, year: int = None) -> Optional[AlbumTrackResponse]:
        """
        Procesa una canción a partir de su ID de video, obteniendo sus detalles.

        Args:
            video_id (dict): El ID del video de YouTube.

        Returns:
            Optional[AlbumTrackResponse]: Los detalles de la canción procesada o None en caso de error.
        """
        try:
            song = self.ytmusic.get_song(track.get("videoId"))
            mc = song.get("microformat", {})
            microformat = mc.get("microformatDataRenderer", {})
            video_details = song.get("videoDetails", {})
            thumbnails = video_details.get("thumbnail", {}).get("thumbnails", [])

            track_response = AlbumTrackResponse(
                response_type=ResponseType.ALBUM_TRACK,
                # Datos obtenidos del primer procesamiento con get_album()
                video_id=track.get("videoId"),
                title=track.get("title"),
                artists=[artist.get("name") for artist in track.get("artists", [])],
                album=track.get("album"),
                track_number=track.get("trackNumber"),
                # Datos de segundo procesamiento con get_song()
                url_canonical=microformat.get("urlCanonical"),
                thumbnail=thumbnails[-1].get("url") if thumbnails else None,
                length_seconds=video_details.get("lengthSeconds"),
                duration_seconds=microformat.get("videoDetails", {}).get("durationSeconds"),
                duration_iso=str(microformat.get("videoDetails", {}).get("durationIso8601")),
                category=microformat.get("category"),
                publish_date=microformat.get("publishDate"),
                upload_date=microformat.get("uploadDate"),
                year=year,
                total_tracks=total_tracks
            )

            return track_response
        except Exception as e:
            self.logger.error(f"Error al obtener la canción con ID {track_response.video_id}: {e}")
            return None        

    def get_tracklist_from_album_playlist_id(self, playlist_id: str) -> Optional[AlbumResponse]:
        """
        Obtiene la lista de canciones de un álbum a partir del ID de su playlist.

        Args:
            playlist_id (str): El ID de la playlist del álbum en YouTube.

        Returns:
            Optional[AlbumResponse]: Los detalles del álbum y su lista de canciones o None en caso de error.
        """
        album_id = self.ytmusic.get_album_browse_id(playlist_id)
        album = self.ytmusic.get_album(album_id)
        album_tracks: List[dict] = album.get("tracks", [])
        try:
            album_response = AlbumResponse(
                response_type=ResponseType.ALBUM,
                title=album.get("title"),
                youtube_type=album.get("type"),
                is_explicit=album.get("isExplicit"),
                year=album.get("year"),
                description=album.get("description"),
                artists=[artist.get("name") for artist in album.get("artists", [])],
                track_count=album.get("trackCount"),
                thumbnail=album.get("thumbnails")[-1].get("url") if album.get("thumbnails") else None,
                tracks=[self.process_track(track, album.get("trackCount"), album.get("year")) for track in album_tracks]
            )

            return album_response
        except Exception as e:
            self.logger.error(f"Error al obtener el álbum desde el ID {album_id}: {e}")
            return None