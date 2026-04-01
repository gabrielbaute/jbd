from app.enums import Bitrate, Format
from app.settings import settings, JBDLogger
from app.managers.download_album_manager import DownloadManager

JBDLogger.setup_logging(level="INFO")

album_playlist_url = "https://music.youtube.com/playlist?list=OLAK5uy_lczVlLnN4R5X3qPrR8qodFYGIdnJ1w354&si=1V9_qweQAz1lIEpa"

manager = DownloadManager(settings=settings)

downloads = manager.download_album(
    album_playlist_url=album_playlist_url,
    genre="Power Metal",
    bitrate=Bitrate.B_128K,
    format=Format.M4A
)

print(downloads.model_dump_json(indent=4))