import csv
from datetime import datetime
from ..constant import NULL
from ..api.naver_api_test import naver_map_LatLng

def processed_data_to_csv(area_Eng, type_code, before_file, after_file):
    processed_data = []
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #? csv 파일 불러와서 영업시간 데이터 전처리
    with open(before_file, "r", encoding="UTF-8") as file:
        csvReader = csv.DictReader(file)
        for shop in csvReader:
            name         = shop["name"]
            type         = shop["type"]
            star_rating  = shop["star_rating"]
            review_total = shop["review_sum"]
            address      = shop["address"]
            contact      = shop["contact"]
            url          = shop["url"]
            latlng       = naver_map_LatLng(address)
            lat          = latlng[0]
            lng          = latlng[1]

            if review_total == NULL:
                review_total = 0

            if address == NULL:
                address_si, address_gu, address_lo, address_detail = NULL, NULL, NULL, NULL
            else:
                address.replace('로',  '로 ')
                address.replace('로  ', '로')
                address_list = address.split()
                address_si     = address_list[0]
                address_gu     = address_list[1]
                address_lo     = address_list[2]
                address_detail = ' '.join(address_list[3:])

            if url == NULL:
                naver_place_id = NULL
            else:
                naver_place_id = url.replace('https://pcmap.place.naver.com/place/','').split('/')[0]


            keys = [
                "name",
                "type_code",
                "type",
                "star_rating",
                "review_total",
                "address_si",
                "address_gu",
                "address_lo",
                "address_detail",
                "area",
                "contact",
                "url",
                "create_time",
                "lat",
                "lng",
                "naver_place_id",
            ]

            values = [
                name,
                type_code,
                type,
                star_rating,
                review_total,
                address_si,
                address_gu,
                address_lo,
                address_detail,
                area_Eng,
                contact,
                url,
                create_time,
                lat,
                lng,
                naver_place_id,
            ]
            processed_data.append(dict(zip(keys, values)))

    # ? csv 파일에 저장
    with open(after_file, "w", encoding="UTF-8") as file:
        csvWriter = csv.DictWriter(file, fieldnames=keys)
        csvWriter.writeheader()
        for row in processed_data:
            csvWriter.writerow(row)

    print(f"{after_file} 생성이 완료되었습니다.")
