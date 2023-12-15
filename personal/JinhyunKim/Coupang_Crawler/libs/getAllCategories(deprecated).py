from requests import get, post
from bs4 import BeautifulSoup
import re


# 대분류 카테고리의 URL을 추출하는 함수
def get_big_categories():
    # 정상적인 크롤링을 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Whale/3.23.214.10 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
    url = "https://www.coupang.com"

    res = get(url, headers=headers, verify=False)   # 정상적인 크롤링을 위한 verify=False 파라미터
    soup = BeautifulSoup(res.text, 'html5lib')

    big_categories=list()

    # 모든 'a' 태그를 순회하며 URL 추출
    for a in soup.find_all('a'):
        try:
            href = a.attrs['href']
            if re.match(r'/np/categories', href):
                big_categories.append('https://www.coupang.com' + href)
            elif re.match(r'/np/campaigns', href):
                big_categories.append('https://www.coupang.com' + href)
        except:
            pass
    return big_categories

# 각 대분류에 대한 소분류 카테고리의 URL을 추출하는 함수
def get_small_categories(big_categories):
    # 정상적인 크롤링을 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Whale/3.23.214.10 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}

    total_categories = list()
    small_categories = list()

    for url in big_categories:
        res = get(url, headers=headers, verify=False)   # 정상적인 크롤링을 위한 verify=False 파라미터
        soup = BeautifulSoup(res.text, 'html5lib')

        try:
            # html 내 모든 'map > area' 선택자를 순회하며 URL
            for i in soup.select('map > area'):
                href = i.attrs['href']
                if re.match('/np/categories', href):
                    small_categories.add('https://www.coupang.com' + href[:21])
                elif re.match('/np/campaigns', href):
                    small_categories.add('https://www.coupang.com' + href[:21])
        except:
            pass

    total_categories = big_categories + small_categories    # 대분류+소분류를 모두 합친 리스트 반환
    return total_categories
