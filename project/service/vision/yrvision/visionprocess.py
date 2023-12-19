from .videopreprocess import clean_filename, download_videos, create_imgframes
from .utils import inference, similarity_result, subject_extraction, key_extraction, insert_result_from_inference, select_result_from_db
import os
import pickle
# from pytube import YouTube

def input_url(model_detect, model_sim, url, fdir, cur):
    '''
    model_detect : object detection model
    model_sim : image similarity model
    url : Youtube url to process
    fdir : folder directory path for downloading the Youtube video -> 한 폴더에 여러 영상 저장되도록 local의 고유 path
    cur : RDB access
    '''
    if not os.path.exists(fdir): # 혹시 폴더 없을수도 있으니 에러 방지
        os.makedirs(fdir)

    video_time = download_videos(fdir, url)
    image_dir = create_imgframes(fdir, url) # image_dir = {fdir}/{url}
    print('videoprocess')
    
    # Detection
    img_list = sorted(os.listdir(image_dir), key = lambda x : int(x[:-4]))
    
    inference_list = list()
    for img in img_list:
        result_list = inference(model_detect, image_dir, img)
        inference_list.extend(result_list)
    
    # img만 들어왔을 때 사용할 inference 결과 pickle 저장
    with open(f'{image_dir}/inference_{url}.pickle' , 'wb') as fp:
        pickle.dump(inference_list, fp, protocol = pickle.HIGHEST_PROTOCOL)
    
    print('detection')
    
    # key category extraction
    video_subject = subject_extraction(inference_list)
    key_result, split_time_list = key_extraction(inference_list, video_time)

    print('key')
    
    # similarity
    similar_itemid_list, category_list = similarity_result(model_sim, key_result, image_dir)
    print('similarity')

    insert_result_from_inference(cur, url, split_time_list, similar_itemid_list, category_list, video_subject)

    print('vision process 저장')

    return 'Successful process'


def input_img(model_sim, url, fdir, image_name, cur):
    '''
    input_url에서 이미 inference process와 result 저장을 진행하기에, img_name(index)만 받으면 해당 추론 결과만 가져오면 된다.
    영상 분할에서 만들어지는 이미지 프레임의 파일 이름(0.jpg ~ (n-1).jpg)는 시간 정보와 file directory 정보를 담고 있기에 매우 중요한 파라미터이다.
    '''
    image_dir = f'{fdir}/{url}'
    with open(f'{image_dir}/inference_{url}.pickle' , 'rb') as fp: # image_dir = {fdir}/{url}
        inference_list = pickle.load(fp)

    image_result = inference_list[int(image_name)]

    similar_itemid_list, category_list = similarity_result(model_sim, image_result, image_dir)
    video_subject = cur.execute("select * from recommendation where url like {0}".format(url)).fetchall()[0][-1]

    return similar_itemid_list, category_list, video_subject