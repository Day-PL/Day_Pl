# selenium webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# data formatter
from .data_formatter import format_date

# data save to excel
from .data_save_to import save_to_xlsx

from ..api.naver_api_test import naver_map_LatLng
from ..api.kakao_api_test import kakao_search_address
from ..constant import NULL

import os
import csv
from datetime import date
from django.utils import timezone

current_dir = os.getcwd()
keys = ['name', 'address_si', 'address_gu', 'address_lo', 'address_detail', 'period_start', 'period_end', 'url', 'created_at', 'lat', 'lng']
file_path = f'{current_dir}/data_process/exhibit_crawler/interpark_csv/exhibit_{date.today()}.csv'

def interpark_crawler():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
    crawler = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    crawler.implicitly_wait(3)
    crawler.get('http://ticket.interpark.com/TiKi/Special/TPRegionReserve.asp?Region=42001&RegionName=%BC%AD%BF%EF#btn_genre_exhibit')

    dls = crawler.find_elements(By.CSS_SELECTOR, 'div.Ltview > div.Gp > div.obj:nth-child(7) > div.Gp > div.content > dl')

    datas = []

    for dl in dls:
        a_tag = dl.find_element(By.CSS_SELECTOR, 'dd.name > p.txt > a')
        name = dl.find_element(By.CSS_SELECTOR, 'dd.name > p.txt > a').text
        url = a_tag.get_attribute('href')
        place = dl.find_element(By.CSS_SELECTOR, 'dd.place > a').text

        address, address_si, address_gu, address_lo = NULL, NULL, NULL, NULL
        address_detail = place

        try: 
                address = kakao_search_address(place, 'CT1')
                address.replace('로', '로 ')
                address.replace('로  ', '로')
                lat, lng = naver_map_LatLng(address)
                address_list = address.split()
                address_si = address_list[0]
                address_gu = address_list[1]
                address_lo = address_list[2]
                address_detail = ' '.join(address_list[3:] + [place])
        except:
            pass

        str_date = dl.find_element(By.CSS_SELECTOR, 'dd.date').text
        period_start, period_end = format_date(str_date)

        created_at = timezone.now()
        values = [name, address_si, address_gu, address_lo, address_detail, period_start, period_end, url, created_at, lat, lng]
        datas.append(dict(zip(keys, values)))
    save_csv(file_path, datas)

def save_csv(file_path, datas):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)

        writer.writeheader()
        for data in datas:
            writer.writerow(data)
    save_to_xlsx(current_dir, file_path, keys)    
