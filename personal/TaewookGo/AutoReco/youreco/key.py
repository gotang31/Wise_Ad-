#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def subject_extraction(inference_list):
    '''
    영상 주제 (Dog or Cat)
    '''
    cat_dog_list = list(map(lambda x: 0 if x[1] == 0 else 1 if x[1] == 1 else None, d))
    
    subject = ''
    dog = cat_dog_list.count(0)
    cat = cat_dog_list.count(1)
    
    if dog > cat:
        subject = 0
        
    elif dog < cat:
        subject = 1
    
    elif dog == cat:
        subject = -1
        
    return subject

def key_extraction(inference_list, video_time):
    '''
    key category extraction
    '''
    # 박스 score 기준으로 내림차순 정렬
    inference_list = sorted(inference_list, key = lambda x : x[2], reverse = true)
    
    # 코드 미완성..
    reco_num = round(video_time // 300) + 1
    key_result = list()
    for obj in inference_list:
        if len(result) == 0:
            result.append(obj)
        else:
            if 
            
    return key_result

