import urllib
import re
import os
import requests
from bs4 import BeautifulSoup
from time import sleep
from urllib.request import urlretrieve, urlopen
import urllib3

import libs.getUrl as getUrl
import libs.createDF as dflib
import libs.importCategories as import_category
import libs.getInfo as getInfo
import libs.downloadimg as downloadimg
import libs.getsubimg as getsubimg
import libs.changeExtension as ce

baseurl = 'https://www.coupang.com/np/categories/'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == '__main__':
    print("get code")
    list = import_category.category_name_list()
    print("coupang category list :",list)
    for name in list:
        ncode = import_category.category_name_to_naver_code(name)
        ccode = import_category.category_name_to_coupang_code(name)
        print("Crawling", name)

        print("create url list")
        url_list = getUrl.get_url_list(ccode, 17)
        print(url_list)

        print("create Dataframe")
        df_new = dflib.create_df()

        print("loop getInfo")
        namelist, categorylist, imglist, pricelist, ratinglist, reviewlist, imgnamelist, linklist = getInfo.loop_url_getinfo(url_list, ccode)
        df_tmp = dflib.fill_df(namelist, categorylist, imglist, pricelist, ratinglist, reviewlist, imgnamelist, linklist)
        df = dflib.concat_df(df_new, df_tmp)

        print("save Dataframe as excel")
        dflib.to_excel(df, ccode)

        print("Download Img")
        downloadimg.download_thumbnail(df, ccode)

        print("download sub image")
        getsubimg.downloadimg(df, ccode)

        print("Extension Change")
        ce.changeextension()

