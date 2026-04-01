import re
from typing import Optional

class ParserService:
    """
    Servicio para extraer y validar IDs desde URLs de YouTube Music.
    
    Se encarga de procesar strings de entrada para obtener identificadores 
    limpios de artistas, álbumes o canciones.
    """

    @staticmethod
    def extract_artist_id(url: str) -> Optional[str]:
        """Extrae el ID del canal del artista desde un link.

        Soporta formatos:
        - https://music.youtube.com/channel/UCevshEcA1yKVc0uucxo4dfg
        - https://music.youtube.com/browse/UCevshEcA1yKVc0uucxo4dfg

        Args:
            url (str): URL completa del canal del artista.

        Returns:
            Optional[str]: El ID del artista (ej. UC...) o None si no coincide.
        """
        # Patrón para identificar IDs de canales de YT (empiezan por UC)
        pattern = r"(?:channel/|browse/)(UC[a-zA-Z0-9_-]+)"
        match = re.search(pattern, url)
        
        return match.group(1) if match else None

    @staticmethod
    def extract_playlist_id(url: str) -> Optional[str]:
        """Extrae el ID de la playlist desde un link.

        Soporta formatos:
        - https://music.youtube.com/watch?v=QCOXCwHmlNo&list=OLAK5uy_nv1s-ojvTwcWH4x-37AGWWW0Fn6-dEsk4
        - https://music.youtube.com/playlist?list=OLAK5uy_nv1s-ojvTwcWH4x-37AGWWW0Fn6-dEsk4
    
        Args:
            url (str): URL completa de la playlist.

        Returns:
            Optional[str]: El ID de la playlist (ej. OLAK...) o None si no coincide.
        """
        # Patrón para identificar IDs de playlists de YT (empiezan por OLAK)
        pattern = r"(?:list=)(OLAK[a-zA-Z0-9_-]+)"
        match = re.search(pattern, url)
        
        return match.group(1) if match else None


    @staticmethod
    def build_track_url(video_id: str) -> str:
        """Construye una URL válida de YouTube a partir de un video_id.

        Args:
            video_id (str): ID único del video/canción.

        Returns:
            str: URL completa lista para yt-dlp.
        """
        return f"https://www.youtube.com/watch?v={video_id}"