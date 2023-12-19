from flask import Flask, request, jsonify
import os
from yrvision.visionmodel import Detr, YouRecoSIm
from yrvision.visionprocess import input_url, input_img
import torch
import psycopg2 as pg

app = Flask(__name__)

# 모델 미리 선언하여 inference 계속 진행될 수 있도록

model_detect = Detr()
ckpt_path = 'epoch=29-step=95610.ckpt'
ckpt = torch.load(ckpt_path, map_location = torch.device('cpu')) # GPU 사용 할 때에는 map_location 삭제 
model_detect.load_state_dict(ckpt['state_dict'])
model_detect.eval()

model_sim = YouRecoSIm()

conn = pg.connect(host="127.0.0.1", dbname="recommendation", user="postgres", password="postgres", port=5432)
cur = conn.cursor()

fdir = '/vision_dir'

# 영상 처리 
@app.route("/infer_url", methods=['POST'])
def process_url():
    if request.method == 'POST': 
        params = request.json
        url = params['url']

        resp = input_url(model_detect, model_sim, url, fdir, cur)

        return resp

@app.route("/infer_img", methods=['POST'])
def process_img():
    if request.method == 'POST': 
        params = request.json
        url = params['url']
        image_name = params['second']

        similar_itemid_list, category_list, video_subject = input_img(model_sim, url, fdir, image_name, cur)

        return jsonify({'similar_itemid_list' : similar_itemid_list, 'category_list': category_list, 'video_subject': video_subject})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))



