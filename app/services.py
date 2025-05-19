import os
import re
import urllib
from pathlib import Path

from mutagen.id3 import TIT2, TALB, TPE1, APIC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment

from pytubefix.exceptions import RegexMatchError, VideoUnavailable

from constants import TEMPORARY_STORAGE_PATH, LIMIT_LENGTH
from exceptions import VideoTooLongError, InvalidUrlError, InvalidVideoError
from models import DownloadRequest, AudioFormat, MetaData


def generate_music(req: DownloadRequest):
    file_path = download_from_youtube(req.url)
    if req.audio_format == AudioFormat.MP3:
        file_path = convert_to_mp3(file_path)

    set_metadata(req.audio_format, file_path, req.metadata)
    return file_path


def download_from_youtube(url: str):
    try:

        youtube = YouTube(url, on_progress_callback=on_progress)
        youtube.check_availability()

        video_length = youtube.length
        if video_length > LIMIT_LENGTH:
            raise VideoTooLongError

        download_thumbnail(youtube)
        return youtube.streams.get_audio_only().download(output_path=TEMPORARY_STORAGE_PATH)

    except RegexMatchError:
        raise InvalidUrlError(url)
    except VideoUnavailable as e:
        raise InvalidVideoError(e.__str__())


def download_thumbnail(youtube):
    if not os.path.exists(TEMPORARY_STORAGE_PATH):
        os.makedirs(TEMPORARY_STORAGE_PATH)
    title = youtube.title
    img_url = youtube.thumbnail_url
    urllib.request.urlretrieve(img_url, f'{TEMPORARY_STORAGE_PATH}/{title}.jpg')


def convert_to_mp3(file_path: str):
    new_file_path = re.sub('m4a$', 'mp3', file_path)
    sound = AudioSegment.from_file(file_path)
    sound.export(new_file_path, format='mp3')
    return new_file_path


def set_metadata(af: AudioFormat, file_path: str, metadata: MetaData):
    title = metadata.title if metadata else None
    album = metadata.album if metadata else None
    artist = metadata.artist if metadata else None
    file_name = Path(file_path).stem
    img_path = f'{TEMPORARY_STORAGE_PATH}/{file_name}.jpg'

    if af == AudioFormat.MP3:
        song = MP3(file_path)
        song.tags.add(APIC(encoding=0, mime='image/jpg', type=3, desc='cover', data=open(img_path, 'rb').read()))
        if title is not None:
            song.tags.add(TIT2(text=title))
        if album is not None:
            song.tags.add(TALB(text=album))
        if artist is not None:
            song.tags.add(TPE1(text=artist))
        song.save()
    elif af == AudioFormat.M4A:
        song = MP4(file_path)
        cover = MP4Cover(open(img_path, 'rb').read(), imageformat=MP4Cover.FORMAT_JPEG)
        song.tags['covr'] = [cover]
        if title is not None:
            song.tags['\xa9nam'] = title
        if album is not None:
            song.tags['\xa9alb'] = album
        if artist is not None:
            song.tags['\xa9ART'] = artist
        song.save()
