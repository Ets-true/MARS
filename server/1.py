import requests
while True:
    print(requests.get("http://localhost").content)
