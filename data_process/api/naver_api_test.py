import urllib.request
import urllib.parse
import json
from ..secret import NAVER_REST_API_CLIENT_SECRET

def naver_api_search_info(query="식껍 종로익선점"):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/local?query=" + encText
    print(url)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", 'CEtfT8cBlzYrf6kqToZ2')
    request.add_header("X-Naver-Client-Secret", NAVER_REST_API_CLIENT_SECRET)

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
            print(item['mapx'], item['mapy'])