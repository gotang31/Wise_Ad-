from .videopreprocess import clean_filename, download_videos, create_imgframes
from .utils import inference, similarity_result, subject_extraction, key_extraction, insert_result_from_inference, select_result_from_db
import os
# import pickle
# from pytube import YouTube

def input_url(model_detect, model_sim, url, fdir, cur):
    '''
    model_detect : object detection model
    model_sim : image similarity model
    url : Youtube url to process
    fdir : folder directory path for downloading the Youtube video -> 한 폴더에 여러 영상 저장되도록 local의 고유 path
    '''
    if not os.path.exists(fdir): # 혹시 폴더 없을수도 있으니 에러 방지
        os.makedirs(fdir)

    video_title, video_time = download_videos(fdir, url)
    image_dir = create_imgframes(fdir, video_title) # image_dir = {fdir}/{video_title}
    print('videoprocess')
    
    # Detection
    # 이미지 시간 순 리스트 : 이미지 저장할 때 0부터 시작해서 저장해야 함
    img_list = sorted(os.listdir(image_dir), key = lambda x : int(x[:-4]))
    
    inference_list = list()
    for img in img_list:
        result_list = inference(model_detect, image_dir, img)
        inference_list.extend(result_list)
    
    print('detection')
    
    # key category extraction
    video_subject = subject_extraction(inference_list)
    key_result, split_time_list = key_extraction(inference_list, video_time)

    print('key')

    # inference result 저장 -> 나중에 단일 이미지 input 될 때 이용하기 위해 ; 사실 이게 영상 추론 DB가 될 수도 있기에 pickle 형식이 아니라 다른 좋은 형식이 있다면 알려주세요.
    # inference_result = {f'{video_title}' : inference_list, 'video_subject' : video_subject}
    # with open(f'{video_title}.pickle' , 'wb') as fp:
    #     pickle.dump(inference_result, fp, protocol = pickle.HIGHEST_PROTOCOL)
    
    # print('inference result 저장')
    
    # similarity
    similar_itemid_list, category_list = similarity_result(model_sim, key_result, image_dir)
    print('similarity')
    print('inference result 저장')

    insert_result_from_inference(cur, url, video_title, video_time, inference_list, split_time_list, similar_itemid_list, category_list, video_subject)

    return similar_itemid_list, category_list, split_time_list, video_subject 


def input_img(model_sim, url, fdir, image_name, cur):
    '''
    input_url에서 이미 inference process와 result 저장을 진행하기에, img_name(index)만 받으면 해당 추론 결과만 가져오면 된다.
    영상 분할에서 만들어지는 이미지 프레임의 파일 이름(0.jpg ~ (n-1).jpg)는 시간 정보와 file directory 정보를 담고 있기에 매우 중요한 파라미터이다.
    '''
    # yt = YouTube(url)
    # video_title = clean_filename(yt.title)

    # with open(f'{fdir}/{video_title}.pickle' , 'rb') as fp:
    #     inference_result = pickle.load(fp)

    row = select_result_from_db(cur, url)
    image_result = row[0][3][image_name]
    video_subject = row[0][-1]
    image_dir = f'{fdir}/{row[0][2]}' # row[0][2] = video_title
    
    similar_itemid_list, category_list = similarity_result(model_sim, image_result, image_dir)

    return similar_itemid_list, category_list, video_subject