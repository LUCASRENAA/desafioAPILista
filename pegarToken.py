import requests
import json
response = requests.post("http://127.0.0.1:8000/^login/",None,{"username":"admin","password":"admin123"}).json()


print(response["token"])

