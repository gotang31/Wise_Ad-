from PIL import Image
from transformers import DetrImageProcessor
import torch

def assign_transform(hubpath):
    image_processor = DetrImageProcessor.from_pretrained(hubpath)
    
    return image_processor
    
def inference(model, fdir, img, hubpath = 'facebook/detr-resnet-50'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    processor = assign_transform(hubpath)
    
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
    cat_dog_list = list(map(lambda x: 0 if x[1] == 0 else 1 if x[1] == 1 else None, inference_list))
    
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
    inference_list = sorted(inference_list, key = lambda x : x[2], reverse = True)
    
    # 코드 미완성..
    reco_num = round(video_time // 300) + 1
    key_result = list()
    for obj in inference_list:
        if len(result) == 0:
            result.append(obj)
        else:
            if 
            
    return key_result
