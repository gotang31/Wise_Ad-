import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.26 Safari/537.36' , 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
loginURL = 'https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F'
loginForm = {'login-email-input': 'ID', 'login-password-input': 'PW'}
init_url = "https://www.coupang.com/np/categories/497141"  # TEST

def getres(url):
    sess = requests.Session()
    # sess.get(loginURL, headers=headers, verify=False)
    # login_request = sess.post(loginURL, data=loginForm)
    res = sess.get(init_url, headers=headers, verify=False)
    text = res.text

    return text

def get_total_page(text):
    soup1 = BeautifulSoup(text, 'html5lib')
    baby_product_list = "".join(soup1.find('ul', {'class': 'baby-product-list'}).get_attribute_list('data-products'))
    page = int(baby_product_list[21:23])

    return page

def get_url_list(page):
    #url 변수 뽑는 함수 필요
    url_list=list()

    for i in range(page):
        url = 'https://www.coupang.com/np/categories/497141/'+str((i+1))
        url_list.append(url)

    return url_list
    print(url_list)