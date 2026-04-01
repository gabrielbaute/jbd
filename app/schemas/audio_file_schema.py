from uuid import UUID
from typing import List
from pathlib import Path
from pydantic import BaseModel, Field

from app.enums import Format

class AudioFile(BaseModel):
    """
    Represents an audio file.
    
    Attributes:
        id (uuid.UUID): ID of the audio file.
        file_path (Path): Path to the audio file.
        file_name (str): Name of the audio file.
        file_format (Format): Format of the audio file.
        file_size (int): Size of the audio file in bytes.
    """
    file_path: Path = Field(..., description="Path to the audio file")
    file_name: str = Field(..., description="Name of the audio file")
    file_format: Format = Field(..., description="Format of the audio file")
    file_size: int = Field(..., description="Size of the audio file in bytes")

class AudioFilesList(BaseModel):
    """
    Represents a list of audio files.
    
    Attributes:
        count (int): Count of files found.
        total_size (int): Total size of files in bytes.
        audio_files (List[AudioFile]): List of audio files.
    """
    count: int = Field(..., description="Count of files found")
    total_size: int = Field(..., description="Total size of files in bytes")
    audio_files: List[AudioFile] = Field(..., description="List of audio files found")