from requests import get, post
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
def get_big_categories():
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
    url = "https://www.coupang.com"

    res = get(url, headers=headers, verify=False)
    soup = BeautifulSoup(res.text, 'html5lib')

    big_categories=list()

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


def get_small_categories(big_categories):
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}

    total_categories = list()
    small_categories = list()

    for url in big_categories:
        res = get(url, headers=headers, verify=False)
        soup = BeautifulSoup(res.text, 'html5lib')

        try:
            for i in soup.select('map > area'):
                href = i.attrs['href']
                if re.match('/np/categories', href):
                    small_categories.add('https://www.coupang.com' + href[:21])
                elif re.match('/np/campaigns', href):
                    small_categories.add('https://www.coupang.com' + href[])
        except:
            pass
