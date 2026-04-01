from enum import StrEnum

class ResponseType(StrEnum):
    """
    Enum que representa los tipos de respuesta para las solicitudes de descarga de música.

    Attributes:
        PLAYLIST (str): Indica que la respuesta es para una playlist.
        TRACK (str): Indica que la respuesta es para una pista individual.
        ARTIST (str): Indica que la respuesta es para un artista.
        ALBUM (str): Indica que la respuesta es para un álbum.
        PLAYLIST_TRACK (str): Indica que la respuesta es para una canción que se extrajo desde el link de una playlist.
        ARTIST_TRACK (str): Indica que la respuesta es para una canción que se extrajo desde el link de un artista.
        ALBUM_TRACK (str): Indica que la respuesta es para una canción que se extrajo desde el link de un álbum.
    """
    PLAYLIST = "playlist"
    TRACK = "track"
    ARTIST = "artist"
    ALBUM = "album"

    PLAYLIST_TRACK = "playlist_track"
    ARTIST_TRACK = "artist_track"
    ALBUM_TRACK = "album_track"