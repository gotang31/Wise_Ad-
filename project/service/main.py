from flask import Flask, request
import os
from yrvision.visionmodel import YouRecoSIm
from yrvision.visionprocess import input_url, input_img

app = Flask(__name__)

# 모델 미리 선언하여 inference 계속 진행될 수 있도록

# model_detect = Detr() # yrvision.model.py에 Detr 모델 코드 넣기
model_sim = YouRecoSIm()
fdir = '영상 저장할 local directory'

@app.route("/", methods=['GET'])
def root():
    a = request.args.get('*')
    return a

@app.route("/ping", methods=['GET'])
def ping():
    return "hi"

# 영상 처리 
@app.route("/infer", methods=['POST'])
def inference():
    if request.method == 'POST': 
        url = "extension에서 url 받았으면 url 담겨있는 문자열, 그냥 이미지면 빈 문자열로 if문 통과하도록" 
        image_name = "extension에서 사용자가 멈출 때 시간의 문자열 넘겨줘야 함"
        
        # url 받을 때
        if url: 
            similar_itemid_list, category_list, video_subject, split_time_list = input_url(model_detect, model_sim, url, fdir)

            return similar_itemid_list, category_list, video_subject, split_time_list
        
        # image 받을 때
        else:
            similar_itemid_list, category_list = input_img(model_sim, url, image_name)

            return similar_itemid_list, category_list

# 추천


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

