import os
import sys
import urllib.request
import urllib.parse
import json
from secret import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

encText = urllib.parse.quote("식껍 종로익선점") #! 예시
url = "https://openapi.naver.com/v1/search/local?query=" + encText

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)

response = urllib.request.urlopen(request)

response_data = response.read().decode('utf-8')
data = json.loads(response_data)

if 'items' in data:
    total_results = data['total']
    for item in data['items']:
        print(item)
        print("이름:", item['title'])
        print("주소:", item['address'])
        print("카테고리:", item['category'])
        print()
