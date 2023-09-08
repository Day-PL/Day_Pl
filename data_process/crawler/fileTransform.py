import pandas as pd
import csv
from ..constant import area_kor_to_eng
from Day_Pl.models import Place, PlaceType


def csv_to_xlsx(csvfile, xlsxfile):
    csvReader = pd.read_csv(csvfile)
    save_xlsx = pd.ExcelWriter(xlsxfile)
    csvReader.to_excel(save_xlsx, index=False)
    save_xlsx.save()

def load_csv(csvfile):
    data = []
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            data.append(row)
    return data

def naver_place_csv_to_db(area_kor, place_type_code):
    area_eng = area_kor_to_eng[area_kor]
    placetype_obj = PlaceType.objects.get(code=place_type_code)
    print(f'종류: {placetype_obj.name}')

    csvfile = f"data_process/csv/{area_eng}_{place_type_code}_processed.csv"
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            search_place  = Place.objects.filter(
                name           = row['name'],
                type_code      = placetype_obj,
                naver_place_id = row['naver_place_id'],
            )

            if len(search_place):
                print(f'존재하는  장소입니다: {search_place.first().name}')
                search_place.update(
                    rating         = row['star_rating'],
                    review_total   = row['review_total'],
                    address_si     = row['address_si'],
                    address_gu     = row['address_gu'],
                    address_lo     = row['address_lo'],
                    address_detail = row['address_detail'],
                    contact        = row['contact'],
                    naver_place_id = row['naver_place_id'],
                )
                print(f'{search_place.first().name} update 완료')

            else:
                print(f'없는 장소입니다.')
                Place.objects.create(
                    name           = row['name'],
                    type_code      = placetype_obj,
                    rating         = row['star_rating'],
                    review_total   = row['review_total'],
                    address_si     = row['address_si'],
                    address_gu     = row['address_gu'],
                    address_lo     = row['address_lo'],
                    address_detail = row['address_detail'],
                    contact        = row['contact'],
                    url            = row['url'],
                    #  period_start = row[''],
                    #  period_end = row[''],
                    created_at = row['create_time'],
                    expected_time_during = 60,
                    lat = row['lat'],
                    lng = row['lng'],
                    naver_place_id = row['naver_place_id']
                )
    # #! 일회용 : db에 naver_place_id 가 https:인거 찾아서 다시 고치는 ORM
    # places = Place.objects.filter(naver_place_id='https:')
    # for place in places:
    #     url = place.url
    #     naver_place_id = url.replace('https://pcmap.place.naver.com/', '').split('/')[1]
    #     place.naver_place_id = naver_place_id
    #     place.save()

    # #! 일회용 : code_big 입력
    # places = Place.objects.all()[1:]
    # for place in places:
    #     print(place.type_code.code[0])
    #     place.type_code_big = place.type_code.code[0]
    #     place.save()