from flask import request
from requests import get, post

# json file response
resp = post('http://172.29.50.29:5000/infer', 'https://www.youtube.com/watch?v=jANE8lpoj2c&t=654s')

