import json
from ytmusicapi import YTMusic

from app.services.parse_service import ParserService
from app.enums.response_type import ResponseType
from app.schemas import PlaylistResponse, TrackResponse

url = "https://music.youtube.com/watch?v=QCOXCwHmlNo&list=OLAK5uy_nv1s-ojvTwcWH4x-37AGWWW0Fn6-dEsk4"

ytmusic = YTMusic()
playlist_id = ParserService.extract_playlist_id(url)
playlist = ytmusic.get_playlist(playlist_id)

tracks = playlist.get("tracks", [])

playlist_response = PlaylistResponse(
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

print(playlist_response.model_dump_json(indent=4))
