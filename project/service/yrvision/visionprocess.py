from .videopreprocess import download_videos, create_imgframes
from .utils import inference, similarity_result, subject_extraction, key_extraction
import os
import pickle


def input_url(model_detect, model_sim, url, fdir):
    '''
    model_detect : object detection model
    model_sim : image similarity model
    url : Youtube url to process
    fdir : folder directory path for downloading the Youtube video -> 한 폴더에 여러 영상 저장되도록 local의 고유 path
    '''
    if not os.path.exists(fdir): # 혹시 폴더 없을수도 있으니 에러 방지
        os.makedirs(fdir)

    video_title, video_time = download_videos(fdir, url)
    image_dir = create_imgframes(fdir, video_title)
    
    # Detection
    # 이미지 시간 순 리스트 : 이미지 저장할 때 0부터 시작해서 저장해야 함
    img_list = sorted(os.listdir(image_dir), key = lambda x : int(x[:-4]))
    
    inference_list = list()
    for img in img_list:
        result_list = inference(model_detect, image_dir, img)
        inference_list.extend(result_list)
    
    # key category extraction
    video_subject = subject_extraction(inference_list)
    key_result, split_time_list = key_extraction(inference_list, video_time)

    # inference result 저장 -> 나중에 단일 이미지 input 될 때 이용하기 위해 ; 사실 이게 영상 추론 DB가 될 수도 있기에 pickle 형식이 아니라 다른 좋은 형식이 있다면 알려주세요.
    inference_result = {f'{image_dir}' : inference_list}
    with open(f'./{url}.pickle' , 'wb') as fp:
        pickle.dump(inference_result, fp, protocol = pickle.HIGHEST_PROTOCOL)
    
    # similarity
    similar_itemid_list, category_list = similarity_result(model_sim, key_result, image_dir)

    return similar_itemid_list, category_list, video_subject, split_time_list


def input_img(model_sim, url, image_name):
    '''
    input_url에서 이미 inference process와 result 저장을 진행하기에, img_name(index)만 받으면 해당 추론 결과만 가져오면 된다.
    영상 분할에서 만들어지는 이미지 프레임의 파일 이름(0.jpg ~ (n-1).jpg)는 시간 정보와 file directory 정보를 담고 있기에 매우 중요한 파라미터이다.
    '''
    with open(f'./{url}.pickle' , 'wb') as fp:
        inference_result = pickle.load(fp)

    image_dir = inference_result.keys()
    image_result = inference_result[image_dir][image_name]
     
    # 같은 물체에 대해서 여러 박스 예측의 경우 어떻게 threshold 설정을 해야할까
    # 우선 한 물체에 대해 박스 하나만 나온다는 이상적인 결과라고 생각
    
    # similarity : 유사도 추론 결과는 저장할 수 없다. image만 받으면 detection 추론 결과를 가지고 유사도 추론은 실시간으로
    similar_itemid_list, category_list = similarity_result(model_sim, image_result, image_dir)

    return similar_itemid_list, category_list