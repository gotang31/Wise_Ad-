import requests
from bs4 import BeautifulSoup


# 정상적인 크롤링을 위한 헤더값 지정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.26 Safari/537.36' , 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}

# (experimental) 인증을 우회하기 위한 방법으로 login 세션 구현
loginURL = r"https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F"
loginForm = {'login-email-input': 'ID', 'login-password-input': 'PW'}   # ID : 사용자의 ID; PW : 사용자의 PW 직접 입력 필요

url = r"https://www.coupang.com/np/categories/502995"    # 크롤링 할 카테고리의 주소 입력!!!

# 크롤링 할 카테고리의 URL로부터 HTML 텍스트를 가져오는 함수
def getres(url):
    sess = requests.Session()
        #   로그인 기능을 구현하려면 아래 두 줄 주석 처리를 풀어야 함
    # sess.get(loginURL, headers=headers, verify=False)
    # login_request = sess.post(loginURL, data=loginForm)

    res = sess.get(url, headers=headers, verify=False)  #   정상적인 크롤링을 위해 verify = False 파라미터 추가
    text = res.text
    
    return text

# 총 페이지 수를 결정하는 함수 (크롤링 진행하며 쿠팡 사이트의 경우 total page 변수가 존재하지만, 이와 상관없이 17페이지까지만 상품 리스트를 제공하는 것을 확인)
def get_total_page(text):
    soup1 = BeautifulSoup(text, 'html5lib')
    baby_product_list = "".join(soup1.find('ul', {'class': 'baby-product-list'}).get_attribute_list('data-products'))
    page = int(baby_product_list[21:23])
    
    return page

# 모든 페이지의 URL 리스트를 생성하는 함수
def get_url_list(page):
    url_list=list()

    for i in range(page):   # 크롤링 진행하며 total page 변수와 상관없이 개인당 17 페이지까지만 상품 리스트를 제공하는 것을 확인. 즉 range(17) 이여도 무방.
        url = r'https://www.coupang.com/np/categories/502995/?page='+str((i+1))  # page 범위 : 1 부터 page (혹은 17)
        url_list.append(url)

    return url_list