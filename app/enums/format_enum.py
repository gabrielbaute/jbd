from typing import List
from enum import StrEnum

class Format(StrEnum):
    """
    Enums para los formatos de audio.

    Attributes:
        MP3 (str): MP3
        WAV (str): WAV
        FLAC (str): FLAC
        OGG (str): OGG
        OPUS (str): OPUS
        AAC (str): AAC
        AIFF (str): AIFF
        M4A (str): M4A
        M4B (str): M4B
    """
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    OGG = "ogg"
    OPUS = "opus"
    AAC = "aac"
    AIFF = "aiff"
    M4A = "m4a"
    M4B = "m4b"

    @staticmethod
    def to_list() -> List[str]:
        return [format.value for format in Format]

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value