#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Input : 이미지 한 장

from youreco.videoprocess import download_videos, create_imgframes
from youreco.key import subject_extraction, key_extraction
from youreco.similarity import SimBck, YouRecoSim
from youreco.utils import inference

# flask에 미리 모델 실행되므로, main에서는 inference만 해주면 된다.
model = Detr()
model_1 = YouRecoSIm()

if __name__ == '__main__':
    
    # front에서 input 받는 부분: image 자체로 input 되는 것인지 혹은 image 파일이 로컬 디렉토리에 저장된 후 input 되는 것인지 결정
    # 로컬 디렉토리에 저장된 후 불러오는 것으로 코드 구현해봤습니다
    
    img = 'image name defined in file directory (format = "0.jpg")'
    img_dir = 'directory where input image is downloaded'
    result_list = inference(model, image_dir, img) 
    # 같은 물체에 대해서 여러 박스 예측의 경우 어떻게 threshold 설정을 해야할까
    # 우선 한 물체에 대해 박스 하나만 나온다는 이상적인 결과라고 생각
    
    # similarity
    similar_item_list = list()                                     # 유사 이미지 상품 itemid
    category_list = list()                                         # 각 object의 classification 결과의 category
    for obj in result_list:
        indices, category = model_1.retrieval_similar(image_dir, obj[0], obj[3])
        similar_item_list.append(indices)
        category_list.append(category)
    
    # similar_item_list는 상품 DB로, category_list는 추천 시스템으로 전달해주는 코드 최종 작성해야 함
    
    # url 입력의 경우 자동 추천이므로, key 물체의 유사 상품을 바로 UI에 바로 띄우지만
    # 이밎 한 장의 경우, 시청자의 능동 상태의 버튼 클릭이 flow에 들어가므로, 이에 대해 UI의 확정 상태일 때 추가적인 코드 작성

