from typing import List
from ytmusicapi import YTMusic
from app.settings import JBDLogger
from app.schemas import AlbumResponse, AlbumTrackResponse
from app.services import DownloaderService, ParserService, YouTubeService

JBDLogger.setup_logging(level="INFO")
yt_music = YTMusic()
youtube_service = YouTubeService()

album_url = "https://music.youtube.com/playlist?list=OLAK5uy_ms71NJ4p7T76oxLP7qnSOVHtNCQlkSqfQ&si=165LRMR1n58O2YOR"

playlist_id = ParserService.extract_playlist_id(url=album_url)
playlist = youtube_service.get_tracklist_from_playlist(playlist_id)
print(playlist)