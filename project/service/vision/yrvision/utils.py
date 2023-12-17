from PIL import Image
from transformers import DetrImageProcessor
import torch


def assign_transform(processor, hubpath):
    image_processor = processor.from_pretrained(hubpath)
    
    return image_processor
    
def inference(model, fdir, img, hubpath = 'facebook/detr-resnet-50'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    processor = assign_transform(DetrImageProcessor, hubpath)
    
    image = Image.open(f'{fdir}/{img}').convert('RGB')

    pixel_values = processor(images = image, return_tensors="pt")
    pixel_values = pixel_values['pixel_values'].to(device)

    with torch.no_grad():
        outputs = model(pixel_values = pixel_values, pixel_mask=None)

    # postprocess model outputs
    width, height = image.size
    postprocessed_outputs = processor.post_process_object_detection(outputs,
                                                                  target_sizes=[(height, width)],
                                                                  threshold = 0.1)
    img_index = int(img[:-4])
    results = postprocessed_outputs[0]
    result_list = list(zip([img_index] * len(results['labels']), results['labels'], results['scores'], results['boxes']))

    return result_list

def similarity_result(model_sim, result_list, image_dir):
    similar_itemid_list = list() # 유사 이미지 상품 itemid
    category_list = list() # 각 object의 classification 결과의 category
    for obj in result_list:
        indices, category = model_sim.retrieval_similar(image_dir, obj[0], obj[3])
        similar_itemid_list.append(indices)
        category_list.append(category)
    
    return similar_itemid_list, category_list

def subject_extraction(inference_list):
    '''
    영상 주제 (Dog or Cat)
    '''
    cat_dog_list = list(filter(lambda x : x[1].item() in [0, 1], inference_list))
    
    subject = ''
    dog = cat_dog_list.count(0)
    cat = cat_dog_list.count(1)
    
    if dog > cat:
        subject = 0
        
    elif dog < cat:
        subject = 1
    
    elif dog == cat: # 이때는 추천에서 어떻게 해결?
        subject = -1
        
    return subject

def key_extraction(inference_list, video_time):
    '''
    key category extraction
    '''
    # 박스 score 기준으로 dog/cat 카테고리 뺀 나머지 카테고리 결과의 내림차순 정렬
    inference_list = sorted(filter(lambda x : x[1].item() not in [0, 1], inference_list), key = lambda x : x[2], reverse = True)

    # Detection category 개수와 추천 최소 시간을 고려한 최적의 구간 개수 및 길이 설정
    reco_min_interval_time = 240   # 초 단위
    category_num_detect = len(set(map(lambda x : x[1], inference_list)))  # # of detected category
    if video_time >= reco_min_interval_time:

        interval_time = video_time / category_num_detect

        while True:
            if interval_time < reco_min_interval_time:
                category_num_detect -= 1
                interval_time = video_time / category_num_detect
            else:
                break

    else:
        interval_time = video_time
        category_num_detect = 1

    # 위에서 나눈 구간에 넣을 카테고리: 그 구간에 들어있지 않아도 시간순으로 카테고리 선정.
    reco_num = category_num_detect
    key_result = list()
    temp = list()                                                   # 중복 카테고리 필터링
    for obj in inference_list:
        if (len(key_result) == 0) or (obj[1].item() not in temp):
            key_result.append(obj)
            temp.append(obj[1].item())

        elif len(key_result) == reco_num:
            break
            
    key_result = sorted(key_result, key = lambda x : x[0])          # 시간순 정렬
    split_time_list = list(round(interval_time) * i for i in range(1, category_num_detect))

    return key_result, split_time_list

# 영상 추론 DB 테이블 틀은 만들어져있다고 생각
def insert_result_from_inference(cursor, url, video_title, video_time, inference_list, split_time_list, similar_itemid_list, category_list, video_subject):
    cursor.execute(
            "INSERT INTO inferenceinfo(url, video_time, inference_list, split_time_list, similar_itemid_list, category_list) VALUES(\'{0}\',{1},{2},{3},{4},{5}, {6}');".format(
                url, video_title, video_time, inference_list, split_time_list, similar_itemid_list, category_list, video_subject))

def select_result_from_db(cursor, url):
    # select 부분 수정 필요
    cursor.execute(f"select * from inferenceinfo where 'url' = {url}")
    row = cursor.fetchall()

    return row