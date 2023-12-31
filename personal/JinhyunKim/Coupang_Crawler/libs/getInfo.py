import pandas as pd
from getUrl import *


# 제품 정보를 저장할 리스트들을 초기화
namelist = list()
imglist = list()
pricelist = list()
ratinglist = list()
reviewlist = list()
linklist = list()

# 웹 페이지의 HTML 문자열로부터 제품 정보를 추출하는 함수
def getinfo(string):
    soup = BeautifulSoup(string, 'html5lib')
    ul = soup.find('ul', {'id':'productList'})  # 제품 목록을 포함하는 ul 태그 찾기
    li = soup.findAll('li', {'class':'baby-product renew-badge'})   # 개별 제품 정보를 포함하는 li 태그 찾기

    for product in li:
        #thumbnail
        dt_class_image = product.find('dt', {'class':'image'})
        img_src = dt_class_image.find('img').get('src')
        imglist.append(img_src)

<<<<<<< HEAD
        #name
        div_class_name = product.find('div',{'class':'name'})
        name_text = div_class_name.getText()
=======
        # 상품명 추출
        div_class_name = product.find('div', {'class':'name'})
        name_text = div_class_name.getText().strip()
>>>>>>> e1fb27c8135956ab028d7650bf249719e386260b
        namelist.append(name_text)

        #price
        strong_class_pricevalue = product.find('strong',{'class':'price-value'})
        price = strong_class_pricevalue.getText()
        pricelist.append(price)

        #rating (별점 없는 제품도 있으므로 예외 처리)
        try:
            em_class_rating = product.find('em', {'class':'rating'})
            rating = em_class_rating.getText()
            ratinglist.append(rating)
        except:
            ratinglist.append(pd.NA)    # 빈 값에 대한 일괄 결측치 처리

        #review_cnt
        try:
            span_class_ratingtotalcount = product.find('span',{'class':'rating-total-count'})
            review_cnt = span_class_ratingtotalcount.getText()
            reviewlist.append(review_cnt)
        except:
            reviewlist.append(pd.NA)
<<<<<<< HEAD

        #url
        a_class_baby_product_link = product.find('a',{'class':'baby-product-link'})
=======
z
        # 상품 URL 추출
        a_class_baby_product_link = product.find('a', {'class':'baby-product-link'})
>>>>>>> e1fb27c8135956ab028d7650bf249719e386260b
        href = a_class_baby_product_link.get('href')
        link = f'https://coupang.com'+href
        linklist.append(link)

# 한 카테고리 내의 여러 page에 대한 URL에서 제품 정보를 추출하고 리스트로 반환
def loop_url_getinfo(url_list):
    for urls in url_list:
        getinfo(getres(urls))

    return namelist,imglist,pricelist,ratinglist,reviewlist,linklist