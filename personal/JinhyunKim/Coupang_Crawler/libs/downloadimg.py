from getUrl import *
from getInfo import *
import os
from urllib.request import urlretrieve, urlopen
import re


# 파일명에 들어갈 수 없는 문자를 지워서 정제하는 함수
def clean_filename(title):
    cleaned_title = re.sub(r'[\/:*?"<>|\s]', '', title)
    return cleaned_title

# BeautifulSoup 객체에서 JPEG URL을 string 형태로 추출하는 함수
def extract_jpeg_urls(soup):
    html_content = str(soup)    # 정규 포현식을 사용해 URL 추출하기 위해 BeautifulSoup 객체를 string 형태로 변환
    matches = re.findall(r'"origin":"(//[^"]+)"', html_content) # 정규 표현식을 사용하여 JPEG 이미지 URL을 추출
    return matches

# 이미지를 다운로드하는 함수
def downloadimg(df):
    for index, row in df.iterrows():    # 데이터프레임의 각 행에 대하여 반복
        link = row['Link']  # 링크를 추출
        name = clean_filename(row['Name'])  # df['Name'] 값을 clean_filename 함수를 통해 정제

        text = (getres(link))   # 링크로부터 requests.get(link) 값 반환
        soup = BeautifulSoup(text, 'html5lib')  # text 변수에 대한 BeautifulSoup 객체를 생성
        jpeg_urls = extract_jpeg_urls(soup) # JPEG URL을 추출


        fdir = f'.//data//sweatshirt//{name}'   # 저장할 디렉토리 경로를 설정
        if not os.path.exists(fdir):    # 디렉토리가 존재하지 않는 경우 생성
            os.makedirs(fdir)

        for urls in jpeg_urls:  # 추출된 모든 URL에 대하여 이미지를 다운로드
            img_url = f'https:{urls}'
            try:
                filename = urls.split('/')[-1]
                file_path = os.path.join(fdir, filename)

                urlretrieve(img_url, file_path) # 이미지 다운로드
                print(f"Downloaded {filename}")

            except Exception as e:  # 오류 발생 시 출력
                print(f"Error downloading {filename}: {e}")