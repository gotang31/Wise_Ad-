from flask import Flask, request,jsonify
import os
from yrvision.visionmodel import Detr, YouRecoSIm
from yrvision.visionprocess import input_url, input_img
import torch

app = Flask(__name__)

# 모델 미리 선언하여 inference 계속 진행될 수 있도록
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_detect = Detr()
ckpt_path = './epoch=29-step=95610.ckpt'
ckpt = torch.load(ckpt_path) # GPU 사용 할 때에는 map_location 삭제 
model_detect.load_state_dict(ckpt['state_dict'])
model_detect.to(device)
model_detect.eval()

model_sim = YouRecoSIm()

fdir = './practice_video'

@app.route("/", methods=['GET'])
def root():
    return 'hello'

@app.route("/ping", methods=['GET'])
def ping():
    return "hi"

# 영상 처리 
@app.route("/infer", methods=['POST'])
def inference():
    if request.method == 'POST': 
        url = str(request.data, 'utf-8')
        image_name = "extension에서 사용자가 멈출 때 시간의 문자열 넘겨줘야 함"
        fdir = './practice_video'
        
        # url 받을 때
        if url: 
            similar_itemid_list, category_list, video_subject, split_time_list = input_url(model_detect, model_sim, url, fdir)

            return jsonify({'similar_itemid_list' : similar_itemid_list, 'category_list': category_list, 
                            'split_time_list' : split_time_list, 'video_subject': video_subject})
        
        # image 받을 때
        else:
            similar_itemid_list, category_list = input_img(model_sim, url, image_name)

            return similar_itemid_list, category_list

# 추천

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)),debug=True)

