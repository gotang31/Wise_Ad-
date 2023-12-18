from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return "root"

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

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