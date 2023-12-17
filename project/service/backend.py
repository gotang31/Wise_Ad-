from flask import request
from requests import get, post

url = 'frontend에서 받는 url' 
image_name = 'frontend에서 받는 image_name'
video_subject = 'url 영상 처리 후, 나온 video_subject'

similar_itemid_list = ''
category_list = ''
split_time_list = ''

# json file response
if url: # 
    resp_vision = post('http://172.29.50.29:5000/infer', url)
    similar_itemid_list = resp_vision['similar_itemid_list']
    category_list = resp_vision['category_list']
    split_time_list = resp_vision['split_time_list']
    video_subject = resp_vision['video_subject']

    resp_reco = post('http://172.29.50.29:5000/infer', json = {'category_list': category_list, 'video_subject': video_subject})

else:
    resp_vision = post('http://172.29.50.29:5000/infer', image_name)
    similar_itemid_list = resp_vision['similar_itemid_list']
    category_list = resp_vision['category_list']
    video_subject = resp_vision['video_subject']

    resp_reco = post('http://172.29.50.29:5000/infer', json = {'category_list': category_list, 'video_subject': video_subject})

