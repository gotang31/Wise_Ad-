import torch
from transformers import DetrForObjectDetection, DetrImageProcessor


def set_device():
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    return DEVICE

def set_image_processor():
    CHECKPOINT = 'facebook/detr-resnet-50'
    image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)
    return image_processor

def set_pretrained_model(DEVICE):
    CHECKPOINT = 'facebook/detr-resnet-50'
    model = DetrForObjectDetection.from_pretrained('facebook/detr-resnet-50')
    model.eval()
    model.to(DEVICE)
    return model

