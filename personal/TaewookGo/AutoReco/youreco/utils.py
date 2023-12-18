#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

