import torch
from PIL import Image, ImageDraw
from libs.model import Detr
from libs.load_huggingface import image_processor, DEVICE
import torchvision.transforms as T


def load_model_from_ckpt():
    ckpt_path = input("학습 체크포인트 파일의 경로를 입력하세요 ex) ./finetuned_model/epoch=29-step=95610.ckpt : ")
    ckpt = torch.load(ckpt_path)

    model = Detr.load_from_checkpoint(ckpt_path)
    model.eval()
    return model

def inference(model):
    image = Image.open(input("테스트 이미지 경로를 입력하세요 ex) ./Test/toilet_test.jpg : ")).convert("RGB")

    inputs = image_processor(images=image, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)

    return image, outputs

def rank_queries(image, outputs, threshold=0.15):
    width, height = image.size
    postprocessed_outputs = image_processor.post_process_object_detection(outputs,target_sizes=[(height, width)],threshold=threshold)
    print(postprocessed_outputs)
    return postprocessed_outputs

def draw_bboxes(image, postprocessed_outputs):
    clean_image = image
    draw = ImageDraw.Draw(clean_image)

    for score, label, box in zip(postprocessed_outputs[0]['scores'], postprocessed_outputs[0]['labels'], postprocessed_outputs[0]['boxes']):
        box = [coordinate.item() for coordinate in box]  # Convert from tensor to list of coordinates
        draw.rectangle(box, outline="red", width=5)
        # Optionally, add the label and score
        draw.text((box[0], box[1]), f"{label.item()} ({score.item():.2f})", fill="red")

    image.show()

def crop_images(image, postprocessed_outputs):
    bounding_boxes = [d['boxes'] for d in postprocessed_outputs]
    cropped_images = list()
    for bbox in bounding_boxes[0]:
        # Each bbox is in the format (x_min, y_min, x_max, y_max)
        left, top, right, bottom = bbox.int()

    # Calculate the height and width from the bounding box
        height = bottom - top
        width = right - left

        # Crop and add to list
        cropped_image = T.functional.crop(image, top.item(), left.item(), height.item(), width.item())
        cropped_images.append(cropped_image)

    return cropped_images

def resize_images(cropped_images, resized_width=224,resized_height=224, ):
    # Define transforms for resizing
    resize = T.Resize(size=(resized_width, resized_height))

    # Create a list for resized images
    resized_images = list()

    # Resize each image in cropped_images list
    for cropped_image in cropped_images:
        resized_image = resize(cropped_image)
        resized_images.append(resized_image)

    return resized_images