from PIL import Image
import torch
import io


def get_prediction(file, image_processor, model, DEVICE):
    
    image = Image.open(file).convert("RGB")
    inputs = image_processor(images=image, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model(**inputs)
    width, height = image.size
    postprocessed_outputs = image_processor.post_process_object_detection(outputs,target_sizes=[(height, width)],threshold=0)
    return postprocessed_outputs

