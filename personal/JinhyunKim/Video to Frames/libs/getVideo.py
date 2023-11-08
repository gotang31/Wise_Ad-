import urllib.request
import re

# 파일명에 포함할  수 없는 문자열 제거
def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title
def save_video(fdir, df) :
    for index, row in df.iterrows():
        title = row['Title']
        filename = clean_filename(title)
        savename = f'{fdir}/{filename}.mp4'

        video_url = row['URL']

        urllib.request.urlretrieve(video_url, savename)
    print("저장완료")