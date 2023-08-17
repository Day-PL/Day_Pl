import csv
import pandas as pd
from datetime import date
from Day_Pl.models import Place, PlaceType

def load_data(file_path):
    datas = []
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for data in reader:
            datas.append(data)
    return datas

def save_to_xlsx(current_dir, file_path, keys):
    df = pd.DataFrame(load_data(file_path), columns=keys)
    df.to_excel(f'{current_dir}/interpark_xlsx/exhibit_{date.today()}.xlsx', index=False)

def save_to_db(file_path):
    placetype_obj = PlaceType.objects.get(code='F4')
    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            search_data = Place.objects.filter(
                name = row['name'],
                type_code = placetype_obj,
                address_si = row['address_si'],
                address_gu = row['address_gu'],
                address_lo = row['address_lo'],
                address_detail = row['address_detail'],
            )
            if search_data:
                search_data.update(
                    period_start = row['period_start'],
                    period_end = row['period_end'],
                    url = row['url'],
                )
            else:
                Place.objects.create(
                    name = row['name'],
                    type_code = placetype_obj,
                    address_si = row['address_si'],
                    address_gu = row['address_gu'],
                    address_lo = row['address_lo'],
                    address_detail = row['address_detail'],
                    period_start = row['period_start'],
                    period_end = row['period_end'],
                    url = row['url'],
                    created_at = row['created_at']
                )