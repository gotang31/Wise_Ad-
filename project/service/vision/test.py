from flask import Flask, request, jsonify
import os
from yrvision.visionmodel import Detr, YouRecoSIm
from yrvision.visionprocess import input_url, input_img
import torch
import psycopg2 as pg
import pickle
from yrvision.videopreprocess import clean_filename, download_videos, create_imgframes
from yrvision.utils import inference, similarity_result, subject_extraction, key_extraction, insert_result_from_inference
import os
import pickle

model_detect = Detr()
ckpt_path = 'epoch=29-step=95610.ckpt'
ckpt = torch.load(ckpt_path, map_location = torch.device('cpu')) # GPU 사용 할 때에는 map_location 삭제 
model_detect.load_state_dict(ckpt['state_dict'])
model_detect.eval()

model_sim = YouRecoSIm()

conn = pg.connect(host="127.0.0.1", dbname="youreco", user="postgres", password="postgres", port=5432)
cur = conn.cursor()

with open(f'vision_dir/HjS9Dz88LjA/inference_HjS9Dz88LjA.pickle' , 'rb') as fp:
        inference_list = pickle.load(fp)
    
print('detection')

# key category extraction
video_subject = subject_extraction(inference_list)
key_result, split_time_list = key_extraction(inference_list, 1073)

print('key')

# similarity
similar_itemid_list, category_list = similarity_result(model_sim, key_result, 'vision_dir/LsPtxoxaDXM')
print('similarity')

print(similar_itemid_list, category_list, split_time_list, key_result, video_subject)

insert_result_from_inference(cur, 'LsPtxoxaDXM', split_time_list, similar_itemid_list, category_list, video_subject)

print('vision process 저장')