import re
from pytube import YouTube
import os

# 파일명에 들어갈 수 없는 문자를 정제하는 함수
def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title

# 유튜브 영상을 다운로드 하는 함수
def download_videos(fdir, df):
    for index, row in df.iterrows():
        title = row['Title']
        cleaned_title = clean_filename(title)
        name = cleaned_title +".mp4"

        url = row['URL']
        yt = YouTube(url)
        yt.streams.get_highest_resolution().download(output_path=fdir, filename=name)
