import requests

BASE = "http://127.0.0.1:5000/"

for i in range(0, 100):
    response = requests.delete(BASE + "video/" + str(i))
    print(response)