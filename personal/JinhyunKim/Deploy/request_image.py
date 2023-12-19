import requests

resp = requests.post("http://127.0.0.1:5000/predict",
                     files={"file": open('C:/Users/jhk16/PycharmProjects/Wise_Ad-/personal/JinhyunKim/Detection_Similarity_Bridge/Test/carrier_test.jpg','rb')})
