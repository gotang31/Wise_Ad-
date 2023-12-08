import os
import shutil

#이미지 파일의 확장자를 .jpg로 통일하는 함수
def changeextension():
    # 'sweatshirt' 폴더 경로 설정
    root_dir = ".//data//cat//hard"

    # 모든 하위 폴더와 파일 탐색
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            # 파일 확장자 확인
            if file.lower().endswith(('.png', '.jpeg', '.gif', '.bmp', '.tiff')):
                # 원본 파일 경로
                original_file_path = os.path.join(subdir, file)
                # 새 파일 경로 (.jpg 확장자 사용)
                new_file_path = os.path.join(subdir, os.path.splitext(file)[0] + '.jpg')

                # 파일 확장자 변경
                shutil.move(original_file_path, new_file_path)