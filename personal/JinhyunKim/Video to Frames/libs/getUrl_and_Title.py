# pip install selenium==4.9.0  to avoid errors with undetected chromedriver
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import math
from bs4 import BeautifulSoup
import pandas as pd
import re


# Selenium 드라이버를 설정하고 로그인을 수행하는 함수
def configure_and_login(channel, loginid, loginpw):
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    time.sleep(1)

    driver.get(f"https://youtube.com/@{channel}/videos")

    # 로그인 코드 추가
    driver.find_element(By.XPATH, '//*[@id="buttons"]/ytd-button-renderer/yt-button-shape/a').click()
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(loginid + Keys.RETURN)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(loginpw + Keys.RETURN)

    return driver


# YouTube 페이지를 스크롤하여 동영상 목록을 더 가져오는 함수
def scroll_down_page(driver, cnt):
    def scroll_down(driver):
        driver.execute_script("window.scrollBy(0, 3000)")  # 한 페이지에 28개씩 출력
        time.sleep(2)

    if cnt <= 28:
        page_cnt = 1
    else:
        page_cnt = math.ceil(cnt / 28)  # 28개의 영상이 한 페이지에 표시된다고 가정

    if cnt > 28:
        for i in range(page_cnt):
            print(f"화면을 {i + 1} 회째 아래로 스크롤 중")
            scroll_down(driver)
            time.sleep(2)

    time.sleep(3)


# YouTube 동영상의 URL 및 제목 수집
def collect_video_urls(driver, cnt):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    item = []
    video_name = []

    for link in soup.find_all('a', 'yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media'):
        item.append(link['href'])
        full_url = ['https://youtube.com' + i for i in item[:cnt]]
        video_name.append(link['title'])

        if len(item) == cnt:
            break

    return full_url, video_name


# 데이터 프레임 생성
def create_dataframe(video_name, full_url):
    df = pd.DataFrame({'Title': video_name, 'URL': full_url})
    return df