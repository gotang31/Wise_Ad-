import requests
from bs4 import BeautifulSoup

# 요청 헤더 설정: 사용자 에이전트 및 언어 설정
headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' , 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}

loginURL = 'https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F'

# 로그인 폼 데이터: ID와 비밀번호 설정 필요
loginForm = {'login-email-input': 'ID', 'login-password-input': 'PW'}

# 테스트 URL 및 실제 URL
init_url = "https://www.coupang.com/np/categories/497141"  # 테스트 URL
url = "https://www.coupang.com/np/categories/119571"  # 고양이화장실 URL

def getres(url):
    # 주어진 URL의 HTML 내용을 가져오는 함수
    sess = requests.Session()
    # 로그인 시도는 현재 주석 처리됨
    # sess.get(loginURL, headers=headers, verify=False)
    # login_request = sess.post(loginURL, data=loginForm)
    res = sess.get(url, headers=headers, verify=False)
    text = res.text
    return text

def get_total_page(text):
    # 가져온 HTML에서 총 페이지 수를 계산하는 함수
    soup1 = BeautifulSoup(text, 'html5lib')
    baby_product_list = "".join(soup1.find('ul', {'class': 'baby-product-list'}).get_attribute_list('data-products'))
    page = int(baby_product_list[21:23])
    return page

def get_url_list(page):
    # 각 페이지에 대한 URL 목록을 생성하는 함수
    url_list = list()
    for i in range(page):
        url = 'https://www.coupang.com/np/categories/119571/?page=' + str((i+1))
        url_list.append(url)
    return url_list
    # URL 목록 출력은 현재 주석 처리됨
    # print(url_list)