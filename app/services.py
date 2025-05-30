import logging
import re
import threading
import time
import urllib
from pathlib import Path

from mutagen.id3 import TIT2, TALB, TPE1, APIC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment

from pytubefix.exceptions import RegexMatchError, VideoUnavailable

from constants import TEMP_STORAGE_PATH, LIMIT_LENGTH, TEMP_FILE_LIVE_TIME_MINUTES
from exceptions import VideoTooLongError, InvalidUrlError, InvalidVideoError
from models import DownloadRequest, AudioFormat, MetaData, FileData


def generate_music(req: DownloadRequest):

    tmp_name = f'{time.strftime('%H%M%S')}_{threading.get_ident()}'
    file_data = FileData(tmp_name=tmp_name)
    download_from_youtube(file_data, req.url)
    if req.audio_format == AudioFormat.MP3:
        convert_to_mp3(file_data)

    set_metadata(req.audio_format, file_data, req.metadata)
    return file_data


def download_from_youtube(file_data: FileData, url: str):
    try:

        youtube = YouTube(url, on_progress_callback=on_progress)
        youtube.check_availability()

        video_length = youtube.length
        if video_length > LIMIT_LENGTH:
            raise VideoTooLongError

        download_thumbnail(file_data, youtube)
        filename = f'{file_data.tmp_name}.m4a'
        file_path = youtube.streams.get_audio_only().download(output_path=TEMP_STORAGE_PATH, filename=filename)
        file_data.output_file_path = file_path

    except RegexMatchError:
        raise InvalidUrlError(url)
    except VideoUnavailable as e:
        raise InvalidVideoError(e.__str__())


def download_thumbnail(file_data: FileData, youtube: YouTube):
    tmp_file_folder = Path(TEMP_STORAGE_PATH)
    if not tmp_file_folder.exists():
        tmp_file_folder.mkdir()
    file_data.output_file_name = youtube.title
    img_url = youtube.thumbnail_url
    urllib.request.urlretrieve(img_url, f'{TEMP_STORAGE_PATH}/{file_data.tmp_name}.jpg')


def convert_to_mp3(file_data: FileData):

    file_path = file_data.output_file_path
    new_file_path = re.sub('m4a$', 'mp3', file_path)
    sound = AudioSegment.from_file(file_path)
    sound.export(new_file_path, format='mp3')
    file_data.output_file_path = new_file_path


def set_metadata(af: AudioFormat, file_data: FileData, metadata: MetaData):

    file_path = file_data.output_file_path
    title = metadata.title if metadata else None
    album = metadata.album if metadata else None
    artist = metadata.artist if metadata else None
    img_path = f'{TEMP_STORAGE_PATH}/{file_data.tmp_name}.jpg'

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

    if title is not None:
        file_data.output_file_name = title
    file_data.output_file_name = f'{file_data.output_file_name}.{'m4a' if af == AudioFormat.M4A else 'mp3'}'


def clean_tmp_folder():

    logging.info('Start clean tmp folder')

    tmp_folder = Path(TEMP_STORAGE_PATH)
    if not tmp_folder.exists() or not tmp_folder.is_dir():
        logging.info('End clean tmp folder, folder not exists')
        return

    deleted_count = 0
    cutoff = time.time() - (TEMP_FILE_LIVE_TIME_MINUTES * 60)

    for f in tmp_folder.iterdir():
        if f.stat().st_mtime < cutoff:
            try:
                f.unlink()
                deleted_count += 1
            except Exception as e:
                logging.error(f'remove {f.name} fail: {e}')

    logging.info(f'End clean tmp folder, remove {deleted_count} files')
