import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 0 設定
API_URL = os.getenv("API_KEY")
USER_DATA = {
    "user_id": "id0",
    "user_name": "Tatsuki",
    "items": [
        {"item_id": 0, "content": "task0"},
        {"item_id": 1, "content": "task1"}
    ]
}
PATCH_DATA = [
        {"item_id": 0, "content": "task0"},
        {"item_id": 1, "content": "task1"},
        {"item_id": 2, "content": "task2"},
    ]

def response_function(response):
    print('url: ', response.url)
    print('status code: ', response.status_code)
    print('response: ', response.json())
    print("--------------------------------------")


# 1 HTTPリクエスト

## 1.1 GETリクエストを送信
print("--------------------------------------")
print("GET")
response = requests.get(API_URL)
response_function(response)
    
## 1.2 POSTリクエストを送信
print("POST")
response = requests.post(API_URL, json=USER_DATA)
response_function(response)

print("GET")
response = requests.get(API_URL)
response_function(response)

USER_URL = os.path.join(API_URL, "id0")

## 1.3 PATCHリクエストを送信
print("PATCH")
response = requests.patch(USER_URL, json=PATCH_DATA)
response_function(response)

print("GET")
response = requests.get(API_URL)
response_function(response)

## 1.4 DELETEリクエストを送信
print("DELETE")
response = requests.delete(USER_URL)
response_function(response)

print("GET")
response = requests.get(API_URL)
response_function(response)
