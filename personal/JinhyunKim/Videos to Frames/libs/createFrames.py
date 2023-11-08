import cv2
import os
import re


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
            exit(0)

        filepath = f'{fdir}/{title}'
        fps = video.get(cv2.CAP_PROP_FPS)

        try:
            if not os.path.exists(filepath[:4]):
                os.makedirs(filepath[:4])
                print(filepath[:4] + " 폴더 생성 완료")
        except:
            print(filepath[:4] + " 폴더를 만들 수 없음")

        count = 0

        while (video.isOpened()):
            ret, image = video.read()
            if (int(video.get(1)) % fps == 0):  # 앞서 불러온 fps 값을 사용하여 1초마다 추출
                cv2.imwrite(filepath[:4] + "/frame%d.jpg" % count, image)
                print('Saved frame number :', str(int(video.get(1))))
                count += 1

        video.release()
