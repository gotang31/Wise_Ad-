from flask import Flask, request
import os
from yrvision.visionmodel import Detr, YouRecoSIm
from yrvision.visionprocess import input_url, input_img

app = Flask(__name__)

# 모델 미리 선언하여 inference 계속 진행될 수 있도록

model_detect = Detr() # yrvision.model.py에 Detr 모델 코드 넣기
model_sim = YouRecoSIm()

@app.route("/", methods=['GET'])
def root():
    a = request.args.get('*')
    return a

@app.route("/ping", methods=['GET'])
def ping():
    return "hi"

@app.route("/add_multiply", methods=['POST'])
def add():
    params = request.json
    num_1 = int(params["param1"])
    num_2 = int(params["param2"])
    add_result = num_1 + num_2
    multiply_result = num_1 * num_2
    print(add_result)
    return [add_result, multiply_result]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

