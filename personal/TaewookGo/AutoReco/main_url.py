#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Input : Youtube url

from youreco.videoprocess import download_videos, create_imgframes
from youreco.key import subject_extraction, key_extraction
from youreco.similarity import similarity_result
from youreco.utils import inference

# flask에 미리 모델 실행되므로, main에서는 inference만 해주면 된다.
model = Detr()
model_1 = YouRecoSIm()

if __name__ == '__main__':
    
    # front에서 input 받는 부분
    url = 'Youtube URL'

    # 영상 분할
    fdir = 'directory for downloading a video' # 비디오 저장 경로

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    video_title, video_time = download_videos(fdir, url)
    image_dir = create_imgframes(fdir, video_title)
    
    # Detection
    # 이미지 시간 순 리스트 : 이미지 저장할 때 0부터 시작해서 저장해야 함
    img_list = sorted(os.ilstdir(image_dir), key = lambda x : int(x[:-4]))
    
    inference_list = list()
    for img in img_list:
        result_list = inference(model, image_dir, img)
        inference_list.extend(result_list)
    
    # key category Extraction
    video_subject = subject_extraction(inference_list)
    key_result = key_extraction(inference_list, video_time)
    
    # similarity
    similar_itemid_list, category_list = similarity_result(model_1, key_result, image_dir)
    
    # similar_item_list는 상품 DB로, category_list는 추천 시스템으로 전달해주는 코드 최종 작성
    

