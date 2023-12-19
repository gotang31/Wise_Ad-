import re
from pytube import YouTube
import os


def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title


def download_videos(fdir, video_name, url):
        cleaned_title = clean_filename(video_name)
        name = cleaned_title +".mp4"

        yt = YouTube(url)
        yt.streams.get_highest_resolution().download(output_path=fdir, filename=name)
