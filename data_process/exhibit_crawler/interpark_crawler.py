# selenium webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BeautifulSoup
from bs4 import BeautifulSoup

# data formatter
from .data_formatter import format_date

# data save to excel
from .data_save_to import save_to_xlsx

from .get_naver_id import get_naver_id

from ..api.naver_api_test import naver_map_LatLng
from ..constant import NULL

import os
import csv
from datetime import date
from django.utils import timezone

current_dir = os.getcwd()
keys = ['name', 'address_si', 'address_gu', 'address_lo', 'address_detail', 'period_start', 'period_end', 'url', 'created_at', 'lat', 'lng', 'naver_place_id']
file_path = f'{current_dir}/data_process/exhibit_crawler/interpark_csv/exhibit_{date.today()}.csv'

def interpark_crawler():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
    service = Service(executable_path=ChromeDriverManager().install())
    crawler = webdriver.Chrome(service=service, options=chrome_options)

    crawler.implicitly_wait(3)
    crawler.get('http://ticket.interpark.com/TiKi/Special/TPRegionReserve.asp?Region=42001&RegionName=%BC%AD%BF%EF#btn_genre_exhibit')

    dls = crawler.find_elements(By.CSS_SELECTOR, 'div.Ltview > div.Gp > div.obj:nth-child(7) > div.Gp > div.content > dl')

    datas = []
    search_keywords = []

    for dl in dls:
        crawler.implicitly_wait(5)
        a_tag = dl.find_element(By.CSS_SELECTOR, 'dd.name > p.txt > a')
        exhibit_name = dl.find_element(By.CSS_SELECTOR, 'dd.name > p.txt > a').text
        url = a_tag.get_attribute('href')
        place = dl.find_element(By.CSS_SELECTOR, 'dd.place > a').text
        name = f'[{place}] {exhibit_name}'

        str_date = dl.find_element(By.CSS_SELECTOR, 'dd.date').text
        period_start, period_end = format_date(str_date)

        a_tag.click()
        wait = WebDriverWait(crawler, 10) 
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#popup-info-place > div > div.popupBody > div > div.popPlaceInfo')))

            # BeautifulSoup으로 html parsing
            page_source = crawler.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            if soup.find('div', class_='popupBody'):
                    try:
                        address = soup.select_one('#popup-info-place > div > div.popupBody > div > div.popPlaceInfo > p:nth-child(2) > span').text
                    except:
                        address = soup.select_one('#popup-info-place > div > div.popupBody > div > div.popPlaceInfo > p > span').text
        except:
            address = NULL

        if address == NULL:
            crawler.back()
            continue

        address_si, address_gu, address_lo = NULL, NULL, NULL
        address_detail = place

        try: 
            if '로' in address:
                address.replace('로', '로 ')
                address.replace('로  ', '로')
            lat, lng = naver_map_LatLng(address)
            address_list = address.split()
            if '서울' not in address_list[0]:
                crawler.back()
                continue
            address_si = '서울특별시'
            address_gu = address_list[1]
            address_lo = address_list[2]
            address_detail = ' '.join(address_list[3:])
        except:
            pass

        place_split = place.split(' ')
        if len(place_split) > 2:
            place_name = place_split[0] + place_split[1]
        else:
            place_name = place_split[0]
        search_keyword = address_si + address_gu + address_lo + place_name
        search_keywords.append(search_keyword)

        crawler.back()

        created_at = timezone.now()
        naver_place_id = NULL
        values = [name, address_si, address_gu, address_lo, address_detail, period_start, period_end, url, created_at, lat, lng, naver_place_id]
        datas.append(dict(zip(keys, values)))
    
    crawler.quit()

    naver_place_ids = get_naver_id(search_keywords)

    indexes_to_remove = []

    for i, naver_place_id in enumerate(naver_place_ids):
        if naver_place_id == NULL:
            indexes_to_remove.append(i)
        datas[i]['naver_place_id'] = naver_place_id

    indexes_to_remove.reverse()
    for index in indexes_to_remove:
        del datas[index]

    save_csv(file_path, datas)

def save_csv(file_path, datas):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)

        writer.writeheader()
        for data in datas:
            writer.writerow(data)
    save_to_xlsx(current_dir, file_path, keys)    
