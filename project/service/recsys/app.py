from flask import Flask, jsonify, request
import os
import main


app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return "root"


@app.route('/ping', methods=['GET'])
def ping():
    return "pong"


@app.route('/recommend', methods=['POST'])
def recommend():
    # request로부터 data를 받습니다.
    data = request.json

    result = main.main(data)
    
    return jsonify(result)


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5012)), debug=True)
