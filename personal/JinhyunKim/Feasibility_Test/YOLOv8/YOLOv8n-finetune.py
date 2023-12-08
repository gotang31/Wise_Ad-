from ultralytics import YOLO
import torch
from PIL import Image


def train_yolo():
    yolo = YOLO('yolov8n.pt')
    yolo.train(data='C://Users//jhk16//PycharmProjects//Wise_Ad-//personal//JinhyunKim//Fiftyone//merged_final_new//dataset.yaml', epochs=10, batch=16,save=True)

def resume_yolo():
    model = YOLO("C://Users//jhk16//PycharmProjects//Wise_Ad-//runs//detect//train9//weights//last.pt")
    results = model.train(data='D:\Data\merged_final\dataset.yaml', epochs=2, batch=32, resume=True,save=True)

def test_yolo():
    # Load the YOLO model
    model = YOLO("C://Users//jhk16//PycharmProjects//Wise_Ad-//runs\detect//train3\weights//best.pt")

    # Run the model on an image
    results = model("C://Users//jhk16//PycharmProjects//Wise_Ad-//personal//JinhyunKim//Fiftyone//YOLOv8//sweatshirt_test.jpg")

    # Show the results
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show()  # show image
        im.save('results.jpg')  # save image

def validate_yolo():
    model = YOLO("C://Users//jhk16//PycharmProjects//Wise_Ad-//runs\detect//train3\weights//best.pt")
    model.val(data="D://Data//Coupang_Sweatshirt_2000.v4i.yolov8//dataset.yaml",plots=True)

if __name__ == '__main__':
    test_yolo()