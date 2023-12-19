from libs.getUrl import *
from libs.getInfo import *
import os
from urllib.request import urlretrieve, urlopen
import re

def clean_filename(title):
    # 파일 이름에서 특수 문자와 공백을 제거하는 함수
    cleaned_title = re.sub(r'[\/:*?"<>|\s]', '', title)
    return cleaned_title

def extract_jpeg_urls(soup):
    # BeautifulSoup 객체를 문자열로 변환
    html_content = str(soup)

    # 정규 표현식을 사용하여 "origin":"//(image URL)" 패턴에 해당하는 모든 URL 추출
    # //(image URL) 부분만 캡처
    matches = re.findall(r'"origin":"(//[^"]+)"', html_content)

    # 추출된 URL 목록 반환
    return matches


def download_thumbnail(df,category):
    # DataFrame의 각 행에 대해 이미지 다운로드 수행
    for index, row in df.iterrows():
        link = row['img_src']
        filename = row['img_src'][-16:-4]

        # 이미지를 저장할 디렉토리 생성
        fdir = f'./data/{category}'
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        # 각 이미지 URL에 대해 다운로드 시도
        try:
            # URL에서 파일명 추출 및 저장 경로 설정
            file_path = os.path.join(fdir, filename)
            filename = category

            # 이미지 다운로드 및 저장
            urlretrieve("https:" + link, file_path + '.jpg')

        except Exception as e:
            # 다운로드 오류 처리
            print(f"Error downloading {filename}: {e}")

def downloadimg(df):
    # DataFrame의 각 행에 대해 이미지 다운로드 수행
    for index, row in df.iterrows():
        link = row['Link']
        # df['Name'] 값 정제
        name = clean_filename(row['Name'])

        text = getres(link)
        soup = BeautifulSoup(text, 'html5lib')
        jpeg_urls = extract_jpeg_urls(soup)

        # 이미지를 저장할 디렉토리 생성
        fdir = f'.//data//cat//toilet//{name}'
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        # 각 이미지 URL에 대해 다운로드 시도
        for urls in jpeg_urls:
            img_url = f'https:{urls}'
            try:
                # URL에서 파일명 추출 및 저장 경로 설정
                filename = urls.split('/')[-1]
                file_path = os.path.join(fdir, filename)

                # 이미지 다운로드 및 저장
                urlretrieve(img_url, file_path)

            except Exception as e:
                # 다운로드 오류 처리
                print(f"Error downloading {filename}: {e}")