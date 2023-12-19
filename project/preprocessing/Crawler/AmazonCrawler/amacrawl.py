from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from urllib.request import urlretrieve
import pandas as pd
import os

# 추천 상품 정보 크롤링
def amazon_prod_url(url, category, max_page):
    browser = webdriver.Chrome()
    browser.get(url)
    sleep(4)
    browser.refresh()
    sleep(4)
    
    hrefs = list() # 상품 페이지 url
    itemname_list = list()
    category_list = list()
    price_list = list()
    rating_list = list()
    reviews_list = list()
    asin_list = list()
    imagefile_list = list() # img hash list
    
    # 상품 진열 페이지에서 각 상품의 url 수집 
    cnt = 0
    while cnt < max_page: # max_page페이지까지만 상품 추출
        
        # 상품 정보 추출
        for i in browser.find_elements(By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]'):
            
            # 상품 url
            href = i.find_element(By.CSS_SELECTOR, 'span[data-component-type="s-product-image"] > a').get_attribute('href')
            hrefs.append(href)
            
            # 상품명
            itemname = i.find_element(By.CSS_SELECTOR, 'span[class="a-size-base-plus a-color-base a-text-normal"]').text
            itemname_list.append(itemname)
            
            # 카테고리
            category_list.append(category)
            
            # 이미지 url
            img = i.find_element(By.CSS_SELECTOR, 'img').get_attribute('srcset').split(', ')
            if img != ['']:
                img = img[1][:-5]
            else:
                img = i.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            
            # Asin : 한 번 넣어봄
            asin = i.get_attribute('data-asin')
            asin_list.append(asin)
            
            # 상품 가격
            try:
                price = i.find_element(By.CSS_SELECTOR, 'span[class="a-price"]').text.replace('\n', '.')
            except:
                price = 'None'
                
            price_list.append(price)

            # Rating/Reviews
            try:
                meta_tag = i.find_elements(By.CSS_SELECTOR, 'div[class="a-row a-size-small"] > span')

                if meta_tag != []:
                    rating = meta_tag[0].get_attribute('aria-label').split(' ')[0]
                    reviews = meta_tag[1].get_attribute('aria-label')
                else:
                    rating, reviews = 'None', 'None'
            except: 
                rating, reviews = 'None', 'None'
            
            rating_list.append(rating)
            reviews_list.append(reviews)

            # 이미지 저장
            img_hash = img.split('/')[-1] # url 생성 시: https://m.media-amazon.com/images/W/MEDIAX_792452-T2/images/I/ 
            imagefile_list.append(img_hash)
            
            fdir = f'recommend/{category}/'
            if not os.path.exists(fdir):
                # 디렉토리가 존재하지 않으면 새로 생성
                os.makedirs(fdir)

            file_path = os.path.join(fdir, img_hash)
            urlretrieve(img, file_path)
        
        if browser.find_elements(By.CSS_SELECTOR, 'span[class="s-pagination-strip"] > span')[-1].text == 'Next':
            break
        
        try:
            next_page = browser.find_elements(By.CSS_SELECTOR, 'span[class="s-pagination-strip"] > a')[-1]
            next_page.click()
            sleep(2)
            cnt += 1
        except:
            break
    
    product_DB = pd.DataFrame({'itemname':itemname_list, 'category': category_list, 'price' : price_list, 
                               'rating' : rating_list, 'reviews': reviews_list, 'asin': asin_list, 'imagefile' : imagefile_list})
    
    browser.close()
    
    return hrefs, product_DB

def amazon_prod_img_down(category, url):
    try:
        browser = webdriver.Chrome()
        browser.get(url)
        sleep(2)
        browser.refresh()
        sleep(2)

        try:
            small = browser.find_elements(By.CSS_SELECTOR, 'li[class="a-spacing-small item imageThumbnail a-declarative"]')
            for sm in small:
                sm.click()

            meta = browser.find_element(By.CSS_SELECTOR, 'ul[class="a-unordered-list a-nostyle a-horizontal list maintain-height"]')
            imgs = meta.find_elements(By.CSS_SELECTOR, 'img')
            try:
                for img in imgs:
                    try:
                        img = img.get_attribute('src')
                        img_hash = img.split('/')[-1]

                        fdir = f'similarity/{category}/'
                        if not os.path.exists(fdir):
                            # 디렉토리가 존재하지 않으면 새로 생성
                            os.makedirs(fdir)

                        file_path = os.path.join(fdir, img_hash)
                        urlretrieve(img, file_path)

                    except:
                        print(f'{url} : 이미지 다운로드 실패')
                        continue
                        
                print(f'{url} : 이미지 다운로드 성공')
                browser.quit()
                
            except:
                
                print(f'{url} : 이미지 다운로드 실패')
                browser.quit()

        except:

            print(f'{url} : 이미지 다운로드 실패')
            browser.quit()
    
    except:
        
        pass
    
    return