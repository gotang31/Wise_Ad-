import re
from pytube import YouTube
import os


def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title


def download_videos(fdir, df):
    for index, row in df.iterrows():
        title = row['Title']
        cleaned_title = clean_filename(title)
        name = cleaned_title +".mp4"

        url = row['URL']
        yt = YouTube(url)
        yt.streams.get_highest_resolution().download(output_path=fdir, filename=name)
