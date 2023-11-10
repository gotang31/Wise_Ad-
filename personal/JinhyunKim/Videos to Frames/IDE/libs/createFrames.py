import cv2
import os
import re
import numpy as np


def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title


def create_imgframes(fdir, df):
    for index, row in df.iterrows():
        title = row['Title']
        cleaned_title = clean_filename(title)
        name = cleaned_title + ".mp4"

        file = f'{fdir}/{name}'
        video = cv2.VideoCapture(file)

        if not video.isOpened():
            print(name, " 영상을 로드할 수 없음")
            continue  # exit(0) 대신 continue 사용

        filepath = f'{fdir}/{cleaned_title}'  # 여기서 cleaned_title을 사용
        fps = video.get(cv2.CAP_PROP_FPS)

        try:
            if not os.path.exists(filepath):
                os.makedirs(filepath)
                print(filepath + " 폴더 생성 완료")
        except OSError as error:
            print(error)
            print(filepath + " 폴더를 만들 수 없음")
            continue  # 폴더 생성에 실패하면 다음 반복으로 넘어감

        count = 0

        while video.isOpened():
            ret, image = video.read()
            if not ret:
                break  # 비디오의 끝이면 종료
            if (int(video.get(1)) % round(fps) == 0):  # 앞서 불러온 fps 값을 사용하여 1초마다 추출
                result, encoded_image = cv2.imencode('.jpg', image)
                if result:
                    frame_filepath = f"{filepath}/frame{count}.jpg"
                    with open(frame_filepath, "wb") as f:  # wb 모드로 바이너리 파일을 연다.
                        f.write(encoded_image)
                    print('Saved frame number :', str(int(video.get(1))))
                    count += 1

        video.release()
