from libs.getInfo import *
import os
from urllib.request import urlretrieve
import re


def clean_filename(title):
    # 파일 이름에서 특수 문자와 공백을 제거하는 함수
    cleaned_title = re.sub(r'[\/:*?"<>|\s]', '', title)
    return cleaned_title


def extract_jpeg_urls(soup):
    # HTML 내용에서 '.jpeg' URL을 추출하는 함수
    # Convert the soup object to a string
    html_content = str(soup)

    # Use regular expression to find all occurrences of "origin":"//(image URL).jpeg"
    # and capture only the //(image URL).jpeg part
    matches = re.findall(r'"origin":"(//[^"]+\.jpeg)"', html_content)

    # Return the list of extracted .jpeg URLs
    return matches


def downloadimg(df,category):
    # DataFrame의 각 행에 대해 이미지를 다운로드하는 함수
    for index, row in df.iterrows():
        # DataFrame의 각 행을 순회
        link = row['Link']
        # 현재 행의 'Link' 값을 가져옴
        name = clean_filename(row['img_name'])
        # 'img_name' 값을 정제하여 파일 이름으로 사용

        text = getres(link)
        # 링크로부터 HTML 내용을 가져옴
        soup = BeautifulSoup(text, 'html5lib')
        # BeautifulSoup을 사용하여 HTML 파싱
        jpeg_urls = extract_jpeg_urls(soup)
        # 파싱된 HTML에서 JPEG URL 추출

        for url in jpeg_urls:
            # 추출된 JPEG URL들을 순회
            filename = url.split('/')[-1]
            # URL의 마지막 부분을 파일명으로 사용

            fdir = f'./data/{category}/{name}'
            # 저장할 디렉토리 경로 설정
            if not os.path.exists(fdir):
                # 디렉토리가 존재하지 않으면 새로 생성
                os.makedirs(fdir)

            file_path = os.path.join(fdir, filename)
            # 최종 파일 경로 조합
            urlretrieve("https:" + url, file_path)
            # 이미지를 다운로드하여 지정된 경로에 저장