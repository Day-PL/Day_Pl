import urllib.parse
import urllib.request
import json
from secret import KAKAO_REST_API_KEY

query = "식껍 종로익선점"
encQuery = urllib.parse.quote(query)

page = 1
size = 15
category_group_code= "FD6" #! 카테고리 = 음식점
count = 0

while True:
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encQuery}&page={page}&size={size}&category_group_code={category_group_code}"

    headers = {
        "Authorization": f'KakaoAK {KAKAO_REST_API_KEY}'
    }

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)

    response_data = response.read().decode('utf-8')
    data = json.loads(response_data)

    if 'documents' in data:
        total_results = data['meta']['total_count']
        print(f'total_results: {total_results}개')
        for item in data['documents']:
            print(item['place_name'])
            print(item['category_name'])
            print(item['phone'])
            print(item['address_name'])
            print(item['road_address_name'])
            print(item['place_url'])
            print()
            count += 1

    if page == data['meta']['pageable_count']:
        break

    page += 1

print(f'총 검색 개수: {count}')