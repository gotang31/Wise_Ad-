#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from createDF import *
from getInfo import *
from getUrl import *
import pandas as pd
import os

def excel_to_list():
    categories_list = pd.read_excel('coupang.csv', usecols='B')[0]
    return categories_list

def main():
    url_meta_list = excel_to_list()
    directory = 'Datasets'                                                                          # 데이터 저장 폴더 이름
    os.mkdir(directory)                                                                             # 현재 작업 디렉토리에 폴더 생성
        
    for url in url_meta_list:
        url_list = get_url_list(url)                                                                # 해당 url 상품 링크에서 페이지 별 링크 리스트
        df_new = create_df()                                                                        # pd.DataFrame 새로 생성
        namelist, imglist, pricelist, ratinglist, reviewlist, linklist = loop_url_getinfo(url_list) # 원하는 상품 데이터 추출
        df_tmp = fill_df(namelist, imglist, pricelist, ratinglist, reviewlist, linklist)            # DataFrame에 데이터 추가
        
        # 수집 데이터 파일 저장(카테고리 분류에 따른 엑셀 파일 저장)
        text = getres(url)
        df = concat_df(df_new,df_tmp)
        dom = BeautifulSoup(text, 'html5lib')
        filename = '_'.join(list(map(lambda x : x.text.strip().replace('/', ',') 
                                     if '/' in x.text.strip() else x.text.strip(), 
                                       dom.select('.search-header > div > div> ul > li'))))         # '쿠팡홈_대분류_중분류_소분류' 형태
        to_excel(df, directory, filename)
        
        print(f'<{filename}> 상품 데이터 수집이 완료되었습니다.')

if __name__== "__main__":
    main()

