from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment
import re

from pytubefix.exceptions import RegexMatchError, VideoUnavailable

from constants import MUSIC_STORAGE_PATH, LIMIT_LENGTH
from exceptions import VideoTooLongError, InvalidUrlError, InvalidVideoError
from models import DownloadInfo


def download(info: DownloadInfo):
    file_path = download_by_pytubefix(info)
    if info.audio_format == 'mp3':
        file_path = convert_to_mp3(file_path)
    return file_path


def download_by_pytubefix(info: DownloadInfo):
    url = info.url
    filename = info.filename + '.' + info.audio_format.lower() if info.filename else None
    try:

        youtube = YouTube(url, on_progress_callback=on_progress)
        youtube.check_availability()
        video_length = youtube.length
        if video_length > LIMIT_LENGTH:
            raise VideoTooLongError
        youtube_stream = youtube.streams.get_audio_only()
        return youtube_stream.download(output_path=MUSIC_STORAGE_PATH, filename=filename)

    except RegexMatchError:
        raise InvalidUrlError(url)
    except VideoUnavailable as e:
        raise InvalidVideoError(e.__str__())


def convert_to_mp3(file_path):
    new_file_path = re.sub('m4a$', 'mp3', file_path)
    sound = AudioSegment.from_file(file_path)
    sound.export(new_file_path, format='mp3')
    return new_file_path
