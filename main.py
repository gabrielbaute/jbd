from app.enums import Bitrate
from app.settings import settings, JBDLogger
from app.schemas.audio_file_schema import AudioFilesList
from app.managers.download_album_manager import DownloadManager

JBDLogger.setup_logging(level="INFO")

album_playlist_url = "https://music.youtube.com/playlist?list=OLAK5uy_mL1LRwDXByMjQJN0XNL0HnLS5bZBYFl2o&si=1dYtoxasOwBR2m2-"

manager = DownloadManager(settings=settings)
downloads = manager.download_album(album_playlist_url=album_playlist_url, genre="Power Metal", bitrate=Bitrate.B_128K)
print(downloads.model_dump_json(indent=4))