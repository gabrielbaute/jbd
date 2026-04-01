import json
from datetime import datetime
from ytmusicapi import YTMusic

from app.enums.response_type import ResponseType
from app.schemas.song_schema import SongResponse

id = "43C0kO6HJ5c"

ytmusic = YTMusic()
song = ytmusic.get_song(id)
mc = song.get("microformat", {})
microformat = mc.get("microformatDataRenderer", {})
video_details = song.get("videoDetails", {})
thumbnails = video_details.get("thumbnail").get("thumbnails", [])

song = SongResponse(
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

print(json.dumps(song.model_dump(), indent=4, default=str))