from flask import request
from requests import get, post

resp = post('http://127.0.0.1:5000/infer', 'https://www.youtube.com/watch?v=jANE8lpoj2c&t=654s')
print(resp)