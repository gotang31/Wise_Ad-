import cv2
import os
import re
import numpy as np

# 파일명에 들어갈 수 없는 문자를 정제하는 함수
def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|]', '', title)
    return cleaned_title

# 이미지를 캡쳐하고 저장하는 함수
def create_imgframes(fdir, df, frame_interval):
    for index, row in df.iterrows():
        title = row['Title']
        cleaned_title = clean_filename(title)
        name = cleaned_title + ".mp4"

        file = f'{fdir}/{name}'
        video = cv2.VideoCapture(file)

        if not video.isOpened():
            print(name, " 영상을 로드할 수 없음")
            continue

        filepath = f'{fdir}/{cleaned_title}'  # 여기서 cleaned_title을 사용
        fps = video.get(cv2.CAP_PROP_FPS)
        print("현재 분석중인 영상의 초당 프레임 수는 : " + str(fps) + " fps 입니다")

        try:
            if not os.path.exists(filepath):
                os.makedirs(filepath)
                print(filepath + " 폴더 생성 완료")
        except OSError as error:
            print(error)
            print(filepath + " 폴더를 만들 수 없음")
            continue  # 폴더 생성에 실패하면 다음 반복으로 넘어감

        # 프레임 간격을 프레임 단위로 변환
        frame_gap = round(fps * frame_interval)
        count = 0
        frame_number = 0

        while video.isOpened():
            ret, image = video.read()
            if not ret:
                break  # 비디오의 끝이면 종료
            if (frame_number % frame_gap == 0):  # 앞서 불러온 fps 값을 사용하여 1초마다 추출
                result, encoded_image = cv2.imencode('.jpg', image)
                if result:
                    frame_filepath = f"{filepath}/frame{count}.jpg"
                    with open(frame_filepath, "wb") as f:  # wb 모드로 바이너리 파일 open.
                        f.write(encoded_image)
                    print('Saved frame number :', frame_number)
                    count += 1

            frame_number += 1

        video.release()
    print("작업 완료! 종료 버튼을 눌러주세요")