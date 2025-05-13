from typing import Optional

from pydantic import BaseModel
from enum import Enum


class AudioFormat(str, Enum):
    M4A = "m4a"
    MP3 = "mp3"


class DownloadInfo(BaseModel):
    url: str
    filename: Optional[str] = None
    audio_format: Optional[AudioFormat] = AudioFormat.MP3

    def __init__(self, url: str, filename: Optional[str] = None, audio_format: Optional[AudioFormat] = AudioFormat.MP3):
        super().__init__(url=url, filename=filename, audio_format=audio_format)
