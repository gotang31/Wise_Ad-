import asyncio
from requests import post

async def send_inference_request(url):
    post('http://127.0.0.1:5000/infer_url', json={'url': url})
    print("request sended")