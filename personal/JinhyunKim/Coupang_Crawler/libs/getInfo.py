import pandas as pd
from getUrl import *

# 상품 정보를 저장할 리스트 초기화
namelist = list()
imglist = list()
pricelist = list()
ratinglist = list()
reviewlist = list()
linklist = list()

def getinfo(string):
    # 주어진 HTML 문자열로부터 상품 정보를 추출하는 함수
    soup = BeautifulSoup(string, 'html5lib')
    ul = soup.find('ul', {'id':'productList'})
    li = soup.findAll('li', {'class':'baby-product renew-badge'})

    for product in li:
        # 썸네일 이미지 추출
        dt_class_image = product.find('dt', {'class':'image'})
        img_src = dt_class_image.find('img').get('src')
        imglist.append(img_src)

        # 상품명 추출
        div_class_name = product.find('div', {'class':'name'})
        name_text = div_class_name.getText().strip()
        namelist.append(name_text)

        # 가격 추출
        strong_class_pricevalue = product.find('strong', {'class':'price-value'})
        price = strong_class_pricevalue.getText()
        pricelist.append(price)

        # 평점 추출 (없는 경우 NA 처리)
        try:
            em_class_rating = product.find('em', {'class':'rating'})
            rating = em_class_rating.getText()
            ratinglist.append(rating)
        except:
            ratinglist.append(pd.NA)

        # 리뷰 수 추출 (없는 경우 NA 처리)
        try:
            span_class_ratingtotalcount = product.find('span', {'class':'rating-total-count'})
            review_cnt = span_class_ratingtotalcount.getText()
            reviewlist.append(review_cnt)
        except:
            reviewlist.append(pd.NA)
z
        # 상품 URL 추출
        a_class_baby_product_link = product.find('a', {'class':'baby-product-link'})
        href = a_class_baby_product_link.get('href')
        link = f'https://coupang.com' + href
        linklist.append(link)

def loop_url_getinfo(url_list):
    # URL 목록을 순회하며 각 URL에서 상품 정보를 추출
    for urls in url_list:
        getinfo(getres(urls))

    # 추출된 모든 상품 정보 반환
    return namelist, imglist, pricelist, ratinglist, reviewlist, linklist