from bs4 import BeautifulSoup
from libs.COUPANG.getUrl import getres
import pandas as pd

namelist = list()
imglist = list()
pricelist = list()
ratinglist = list()
reviewlist = list()

def getinfo(string):
    soup = BeautifulSoup(string, 'html5lib')
    ul = soup.find('ul', {'id':'productList'})
    li = soup.findAll('li', {'class':'baby-product renew-badge'})

    for product in li:
        #thumbnail
        dt_class_image = product.find('dt', {'class':'image'})
        img_src = dt_class_image.find('img').get('src')
        imglist.append(img_src)

        #name
        div_class_name = product.find('div',{'class':'name'})
        name_text = div_class_name.getText()
        namelist.append(name_text)

        #price
        strong_class_pricevalue = product.find('strong',{'class':'price-value'})
        price = strong_class_pricevalue.getText()
        pricelist.append(price)

        #rating
        try:
            em_class_rating = product.find('em', {'class':'rating'})
            rating = em_class_rating.getText()
            ratinglist.append(rating)
        except:
            ratinglist.append(pd.NA)

        #review_cnt
        try:
            span_class_ratingtotalcount = product.find('span',{'class':'rating-total-count'})
            review_cnt = span_class_ratingtotalcount.getText()
            reviewlist.append(review_cnt)
        except:
            reviewlist.append(pd.NA)



def loop_url_getinfo(url_list):
    for urls in url_list:
        getinfo(getres(urls))

    return namelist,imglist,pricelist,ratinglist,reviewlist