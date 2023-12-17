from pytube import YouTube
import cv2
import os
import re


def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title


def download_videos(fdir, url):
    yt = YouTube(url)
    video_title = clean_filename(yt.title)
    video_time = yt.length
    yt.streams.get_highest_resolution().download(output_path = fdir, filename = video_title )
    
    return video_title, video_time

def create_imgframes(fdir, title):
    file = f'{fdir}/{title}'
    video = cv2.VideoCapture(file)
    
    if not video.isOpened():
        exit()
    
    # Image folder directory path
    filepath = f'{fdir}/{title}'  
    
    fps = video.get(cv2.CAP_PROP_FPS)

    # 새로운 이미지 담는 폴더 생성
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)

    except OSError as error:
        print(error)
        exit()
        
    count = 0

    while video.isOpened():
        ret, image = video.read()
        if not ret:
            break  # 비디오의 끝이면 종료
        if (int(video.get(1)) % round(fps) == 0):  # 앞서 불러온 fps 값을 사용하여 1초마다 추출
            result, encoded_image = cv2.imencode('.jpg', image)
            if result:
                frame_filepath = f"{filepath}/{count}.jpg"
                with open(frame_filepath, "wb") as f:  # wb 모드로 바이너리 파일을 연다.
                    f.write(encoded_image)
                count += 1

    video.release()
    
    return filepath

