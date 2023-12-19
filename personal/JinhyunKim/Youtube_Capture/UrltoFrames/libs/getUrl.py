import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import math
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Selenium 드라이버를 설정하고 로그인을 수행하는 함수
def configure_uc(url):
    driver = uc.Chrome(driver_executable_path=resource_path("undetected_chromedriver.exe"))
    driver.implicitly_wait(7)
    driver.maximize_window()
    time.sleep(1)
    driver.refresh()
    driver.get(url)
    driver.refresh()

    # # 로그인 코드 추가
    # driver.find_element(By.XPATH, '//*[@id="buttons"]/ytd-button-renderer/yt-button-shape/a').click()
    # driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(ID + Keys.RETURN)
    # time.sleep(2)
    # driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(PW + Keys.RETURN)

    time.sleep(3)

    return driver

# YouTube 동영상의 URL 및 제목 수집
def collect_video_urls(driver):
    video_name = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text

    driver.close()
    time.sleep(1)

    return video_name