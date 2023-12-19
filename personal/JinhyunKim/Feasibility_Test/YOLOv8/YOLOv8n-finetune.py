from ultralytics import YOLO
import torch
from PIL import Image


# yolo v8 nano 모델 파인튜닝 함수
def train_yolo():
    yolo = YOLO('yolov8n.pt')   # pretrained 된 모델 지정
    yolo.train(data='D://Data//merged_final_new//dataset.yaml', epochs=10, batch=16,save=True)   # Custom 데이터셋의 yaml 파일 지정

# 중단된 시점부터 학습 재개하는 함수
def resume_yolo():
    model = YOLO(".//runs//detect//train9//weights//last.pt") # 저장된 pretrained model 디렉토리 지정
    results = model.train(data='D://Data//merged_final_new//dataset.yaml', epochs=2, batch=32, resume=True,save=True)   # Custom 데이터셋의 yaml 파일 지정

# 파인튜닝 된 모델로부터 Inference Test 진행하는 함수
def test_yolo():
    model = YOLO("C://Users//jhk16//PycharmProjects//Wise_Ad-//runs\detect//train3\weights//best.pt")   # 파인튜닝 된 모델 지정
    results = model(".//Inference_Test//sweatshirt_test.jpg")

    # 사진 위에 Inference 결과 표시
    for r in results:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])
        im.show()
        im.save('results.jpg')  # 결과 사진 저장

# 파인튜닝 된 모델에 대한 성능 평가 metrics 추출
def validate_yolo():
    model = YOLO("C://Users//jhk16//PycharmProjects//Wise_Ad-//runs\detect//train3\weights//best.pt")   # 파인튜닝 된 모델 지정
    model.val(data="D://Data//Coupang_Sweatshirt_2000.v4i.yolov8//dataset.yaml",plots=True) # 성능 평가에 사용할 데이터셋 yaml 파일 지정

if __name__ == '__main__':
    test_yolo()