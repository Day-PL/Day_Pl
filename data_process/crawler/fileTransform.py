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
    print(placetype_obj)

    csvfile = f"data_process/csv/{area_eng}_{place_type_code}_processed.csv"
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            search_place  = Place.objects.filter(
                name           = row['name'],
                type_code      = placetype_obj,
                naver_place_id = row['naver_place_id'],
                # address_si     = row['address_si'],
                # address_gu     = row['address_gu'],
                # address_lo     = row['address_lo'],
                # address_detail = row['address_detail'],
                # contact        = row['contact']
                )
            print('찾은 장소: ', search_place)
            if search_place:
                search_place.update(
                    rating         = row['star_rating'],
                    review_total   = row['review_total'],
                    address_si     = row['address_si'],
                    address_gu     = row['address_gu'],
                    address_lo     = row['address_lo'],
                    address_detail = row['address_detail'],
                    contact        = row['contact']
                    )
            else:
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
                    expected_time_during = 60,
                    created_at = row['create_time'],
                    lat = row['lat'],
                    lng = row['lng'],
                    naver_place_id = row['naver_place_id']
                    )
