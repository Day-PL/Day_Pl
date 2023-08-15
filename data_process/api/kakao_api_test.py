import urllib.parse
import urllib.request
import json
import requests
from secret import KAKAO_REST_API_KEY


#! 식당: "FD6"  관광명소: "AT4"  문화시설: "CT1"
def kakao_search_address(search_keyword, category_group_code='', page=1, size=1):
    encQuery = urllib.parse.quote(search_keyword)
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encQuery}&page={page}&size={size}"
    if category_group_code:
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encQuery}&page={page}&size={size}&category_group_code={category_group_code}"
        
    request = urllib.request.Request(url, headers={"Authorization": f'KakaoAK {KAKAO_REST_API_KEY}'})
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
            print(f"지번주소: {item['address_name']}\n도로명주소: {item['road_address_name']}")
            return item['address_name'], item['road_address_name'] #! 도로명

# kakao_search_address("예술의전당 한가람미술관", "CT1")


#! KoGPT API 호출을 위한 메서드 선언
#! 각 파라미터 기본값으로 설정
def kogpt_api(prompt, max_tokens = 1, temperature = 1.0, top_p = 1.0, n = 1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers = {
            'Authorization': 'KakaoAK ' + KAKAO_REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    #! 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

#! KoGPT에게 전달할 명령어 구성
prompt = ''' "서울 종로구 돈화문로11다길 34 세컨디포레스트 익선점"에서 "서울 중구 을지로12길 29 2층"까지 대중교통과 걷는 것을 이용해서 얼마나 걸리는 지 알려줘'''

#! 파라미터를 전달해 kogpt_api()메서드 호출
response = kogpt_api(
    prompt = prompt,
    max_tokens = 32,
    temperature = 0.5,
    top_p = 0.5,
    n = 3
)

print(response)


# page = 1
# size = 15
# category_group_code= "FD6" #! 카테고리 = 음식점
# count = 0

# while True:
#     # url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encQuery}&page={page}&size={size}&category_group_code={category_group_code}"
#     url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={encQuery}&page={page}&size={size}"

#     headers = {
#         "Authorization": f'KakaoAK {KAKAO_REST_API_KEY}'
#     }

#     request = urllib.request.Request(url, headers=headers)
#     response = urllib.request.urlopen(request)

#     response_data = response.read().decode('utf-8')
#     data = json.loads(response_data)

#     if 'documents' in data:
#         total_results = data['meta']['total_count']
#         print(f'total_results: {total_results}개')
#         for item in data['documents']:
#             print(item['place_name'])
#             print(item['category_name'])
#             print(item['phone'])
#             print(item['address_name'])
#             print(item['road_address_name'])
#             print(item['place_url'])
#             print()
#             count += 1

#     if page >= data['meta']['pageable_count']:
#         break

#     page += 1

# print(f'총 검색 개수: {count}')
