from typing import Optional

from pydantic import BaseModel
from enum import Enum


class AudioFormat(str, Enum):
    M4A = "m4a"
    MP3 = "mp3"


class MetaData(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None


class DownloadRequest(BaseModel):
    url: str
    audio_format: Optional[AudioFormat] = AudioFormat.M4A
    metadata: Optional[MetaData] = None

    def __init__(self, url: str, audio_format: Optional[AudioFormat] = AudioFormat.M4A,
                 metadata: Optional[MetaData] = None):
        super().__init__(url=url, audio_format=audio_format, metadata=metadata)


class FileData(BaseModel):
    tmp_name: str
    output_file_name: Optional[str] = None
    output_file_path: Optional[str] = None

    def __init__(self, tmp_name: str):
        super().__init__(tmp_name=tmp_name)
