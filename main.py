from app.enums import Bitrate
from app.settings import settings, JBDLogger
from app.services import DownloaderService, YouTubeService, ParserService

JBDLogger.setup_logging(level="INFO")

album_playlist_url = "https://music.youtube.com/playlist?list=OLAK5uy_l8bkEhA0QRW2fu8D-XnXMte9vqxqveMQg&si=u-L2boIsdW5DkWP6"

youtube_service = YouTubeService()
album_id = ParserService.extract_playlist_id(album_playlist_url)

album_info = youtube_service.get_tracklist_from_album_playlist_id(album_id)
downloader_service = DownloaderService(settings, album_info)
downloader_service.download_album_to_mp3(bitrate=Bitrate.B_128K, genre="Power Metal")