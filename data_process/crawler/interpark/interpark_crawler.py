# selenium webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# data formatter
from data_formatter import format_date

# data save to excel
from data_save_to_excel import save_to_excel

import os
import csv
from datetime import date

current_dir = os.getcwd()

def save_csv(file_path, datas):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)

        writer.writeheader()
        for data in datas:
            writer.writerow(data)

def interpark_crawler():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    crawler = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    crawler = webdriver.Chrome(options=chrome_options)

    crawler.implicitly_wait(3)
    crawler.get('http://ticket.interpark.com/TiKi/Special/TPRegionReserve.asp?Region=42001&RegionName=%BC%AD%BF%EF#btn_genre_exhibit')

    dls = crawler.find_elements(By.CSS_SELECTOR, 'div.Ltview > div.Gp > div.obj:nth-child(7) > div.Gp > div.content > dl')

    datas = []

    for dl in dls:
        aTag = dl.find_element(By.CSS_SELECTOR, 'dd.name > p.txt > a')
        name = dl.find_element(By.CSS_SELECTOR, 'dd.name > p.txt > a').text
        url = aTag.get_attribute('href')
        place = dl.find_element(By.CSS_SELECTOR, 'dd.place > a').text

        str_date = dl.find_element(By.CSS_SELECTOR, 'dd.date').text
        start_date, end_date = format_date(str_date)

        values = [name, place, start_date, end_date, url]
        datas.append(dict(zip(keys, values)))

    save_csv(file_path, datas)
    save_to_excel(current_dir, file_path, keys)

if __name__ == "__main__":
    keys = ['name', 'place', 'start_date', 'end_date', 'url']
    file_path = f'{current_dir}/interpark_csv/exhibit_{date.today()}.csv'
    interpark_crawler()