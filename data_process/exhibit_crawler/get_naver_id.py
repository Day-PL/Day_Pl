from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from ..constant import NULL

from bs4 import BeautifulSoup

import time

def get_naver_id(search_keywords):
    naver_place_ids = []

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
    service = Service(executable_path=ChromeDriverManager().install())
    crawler = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://map.naver.com/p'

    for search_keyword in search_keywords:
        crawler.get(url)
        time.sleep(2)

        search_box = crawler.find_element(By.CLASS_NAME, "input_search")
        search_box.send_keys(search_keyword)
        search_box.send_keys(Keys.ENTER)

        crawler.implicitly_wait(2)
        page_source = crawler.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        try:
            if soup.find('iframe', id='entryIframe'):
                crawler.switch_to.default_content()
                entryIframe = crawler.find_element(By.ID, "entryIframe")
                crawler.switch_to.frame(entryIframe)
                time.sleep(2)
                page_source = crawler.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                current_url = soup.find('meta', {'id': 'og:url'}).get('content')
            else:
                time.sleep(2)
                searchIframe = crawler.find_element(By.ID, "searchIframe")
                crawler.switch_to.frame(searchIframe)
                time.sleep(2)

                crawler.find_element(By.CSS_SELECTOR, ".ApCpt:nth-child(1)").click()

                crawler.switch_to.default_content()
                entryIframe = crawler.find_element(By.ID, "entryIframe")
                crawler.switch_to.frame(entryIframe)
                time.sleep(2)
                page_source = crawler.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                current_url = soup.find('meta', {'id': 'og:url'}).get('content')
        except:
            current_url = ''
        
        if current_url != '':
            naver_place_id = current_url.replace('https://pcmap.place.naver.com/', '').split('/')[1]
        else:
            naver_place_id = NULL
        
        naver_place_ids.append(naver_place_id)

    crawler.quit()
    return naver_place_ids
