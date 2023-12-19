import pandas as pd
from libs.getUrl import *


def getinfo(string, category):
    # 상품 정보를 저장할 리스트 초기화
    namelist = list()
    categorylist = list()
    imglist = list()
    pricelist = list()
    ratinglist = list()
    reviewlist = list()
    imgnamelist = list()
    linklist = list()

    # 주어진 HTML 문자열로부터 상품 정보를 추출하는 함수
    soup = BeautifulSoup(string, 'html5lib')
    li = soup.findAll('li', {'class':'baby-product renew-badge'})

    for product in li:
        # 썸네일 이미지 추출 / 이미지파일 이름 추출
        dt_class_image = product.find('dt', {'class':'image'})
        img_src = dt_class_image.find('img').get('src')
        imglist.append(img_src)
        imgnamelist.append(img_src[-16:-4])

        # 상품명 추출
        div_class_name = product.find('div', {'class':'name'})
        name_text = div_class_name.getText().strip()
        namelist.append(name_text)

        #카테고리 입력
        categorylist.append(category)

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
        

        # 상품 URL 추출
        a_class_baby_product_link = product.find('a', {'class':'baby-product-link'})
        href = a_class_baby_product_link.get('href')
        link = f'https://coupang.com' + href
        linklist.append(link)

    return namelist, categorylist, imglist, pricelist, ratinglist, reviewlist, imgnamelist, linklist


def loop_url_getinfo(url_list, category):
    # 상품 정보를 저장할 리스트 초기화
    namelist_tot = list()
    category_tot = list()
    imglist_tot = list()
    pricelist_tot = list()
    ratinglist_tot = list()
    reviewlist_tot = list()
    imgnamelist_tot = list()
    linklist_tot = list()

    # URL 목록을 순회하며 각 URL에서 상품 정보를 추출
    for urls in url_list:
        namelist, categorylist, imglist, pricelist, ratinglist, reviewlist, imgnamelist, linklist = getinfo(getres(urls), category)
        namelist_tot += namelist
        category_tot += categorylist
        imglist_tot += imglist
        pricelist_tot += pricelist
        ratinglist_tot += ratinglist
        reviewlist_tot += reviewlist
        imgnamelist_tot += imgnamelist
        linklist_tot += linklist

    # 추출된 모든 상품 정보 반환
    return namelist_tot, category_tot, imglist_tot, pricelist_tot, ratinglist_tot, reviewlist_tot, imgnamelist_tot, linklist_tot