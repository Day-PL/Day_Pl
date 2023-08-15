import os
import csv
import requests
from bs4 import BeautifulSoup
from secret import KOPIS_REST_API_KEY

page = 1
total = 10
response = requests.get(f'http://www.kopis.or.kr/openApi/restful/pblprfr?service={KOPIS_REST_API_KEY}&rows={total}&cpage={page}&prfstate=02&signgucode=11')
# 진행 중인 공연 : prfstate=02
# 서울특별시 공연만 : signgucode=11

def save_xml(file_path, data):
    with open(f'{file_path}.xml', "w") as file:
        file.write(data)

def load_xml(file_path):
    with open(f'{file_path}.xml', 'r', encoding='utf-8') as file:
        xml_data = file.read()
    return xml_data

def parse_xml(xml_data):
    soup = BeautifulSoup(xml_data, 'lxml')
    datas = soup.find_all('db')

    result = []
    keys = ['name', 'place', 'start_date', 'end_date']

    for data in datas:
        name = data.find('prfnm').get_text()
        place = data.find('fcltynm').get_text()
        start_date = data.find('prfpdfrom').get_text()
        end_date = data.find('prfpdto').get_text()
        values = [name, place, start_date, end_date]
        result.append(dict(zip(keys, values)))
    return result