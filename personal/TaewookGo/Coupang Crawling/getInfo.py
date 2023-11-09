#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from getUrl import *
from bs4 import BeautifulSoup
import pandas as pd
import re

def getinfo(string, namelist, imglist, pricelist, ratinglist, reviewlist, linklist): # 상품 데이터 수집
    soup = BeautifulSoup(string, 'html5lib')
    ul = soup.find('ul', {'id':'productList'})
    li = soup.findAll('li', {'class':'baby-product renew-badge'})

    for product in li:
        # thumbnail
        dt_class_image = product.find('dt', {'class':'image'})
        img_src = dt_class_image.find('img').get('src')
        imglist.append(img_src)

        # name
        div_class_name = product.find('div',{'class':'name'})
        name_text = re.sub(r'[\/:*?"<>|]', '_', div_class_name.getText()).strip()
        namelist.append(name_text)

        # link
        href = product.find('a').attrs['href']
        linklist.append('https://www.coupang.com' + href)
        
        # price
        try:    
            strong_class_pricevalue = product.find('strong',{'class':'price-value'})
            price = strong_class_pricevalue.getText()
            pricelist.append(price)
        except:
            pricelist.append(pd.NA)
            
        # rating
        try:
            em_class_rating = product.find('em', {'class':'rating'})
            rating = em_class_rating.getText()
            ratinglist.append(rating)
        except:
            ratinglist.append(pd.NA)

        # review_cnt
        try:
            span_class_ratingtotalcount = product.find('span',{'class':'rating-total-count'})
            review_cnt = span_class_ratingtotalcount.getText()
            reviewlist.append(review_cnt)
        except:
            reviewlist.append(pd.NA)


def loop_url_getinfo(url_list): # url_list: excel -> list로 변환한 링크 모음
    namelist = list()
    imglist = list()
    pricelist = list()
    ratinglist = list()
    reviewlist = list()
    linklist = list()
    
    for urls in url_list:
        getinfo(getres(urls), namelist, imglist, pricelist, ratinglist, reviewlist, linklist)

    return namelist, imglist, pricelist, ratinglist, reviewlist, linklist

