from libs.load_huggingface import *
from libs.model import *
from libs.data import *
from libs.utils import *



def main():
    model = load_model_from_ckpt()
    image, outputs = inference(model)
    postprocessed_outputs = rank_queries(image, outputs, threshold=0.15)
    draw_bboxes(image, postprocessed_outputs)
    cropped_images = crop_images(image, postprocessed_outputs)
    resized_images = resize_images(cropped_images, 224,224)
    print(resized_images)

if __name__ == "__main__":
    main()