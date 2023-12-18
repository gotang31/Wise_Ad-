#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.26 Safari/537.36' , 
           'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}

def getres(url):
    sess = requests.Session()
    res = sess.get(url, headers=headers, verify=False)
    text = res.text
    
    return text

def get_url_list(url):
    url_list=list()

    for i in range(1,18):
        url_pg = url + '?page=' + str((i))
        url_list.append(url_pg)

    return url_list

