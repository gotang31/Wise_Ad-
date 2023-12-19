from flask import Flask, jsonify, request
#from libs.utils import set_device, set_image_processor, set_pretrained_model
from libs.inference import get_prediction
from transformers import DetrForObjectDetection, DetrImageProcessor
import torch
from PIL import Image
import io


app = Flask(__name__)

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
CHECKPOINT = 'facebook/detr-resnet-50'
image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)
model = DetrForObjectDetection.from_pretrained('facebook/detr-resnet-50')
model.eval()
model.to(DEVICE)

@app.route('/', methods = ['GET'])
def initiate():
    return "Model loaded"

@app.route('/predict', methods=['POST'])

def predict():
    if request.method == 'POST':
        file = request.files['file']
        postprocessed_outputs = get_prediction(file, image_processor, model, DEVICE)
        scores = postprocessed_outputs['scores'].tolist()
        labels = postprocessed_outputs['labels'].tolist()
        boxes = postprocessed_outputs['boxes'].tolist()
        print(postprocessed_outputs)
        return jsonify({"scores": scores, "labels": labels, "boxes": boxes})

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
