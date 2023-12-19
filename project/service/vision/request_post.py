from requests import get, post

# json file response
resp = post('http://127.0.0.1:5000/infer_url', json = {'url': 'HjS9Dz88LjA'})
print(resp)
