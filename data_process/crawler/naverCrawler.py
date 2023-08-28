from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
from ..constant import area_kor_to_eng, type_searchname_to_typecode, NULL


# ? 페이지의 맨 밑까지 스크롤 (맥 + 34인치 모니터 기준/ 한페이지에 55개 상점 정보)
def scroll_down(crawler):
    for _ in range(10):
        body = crawler.find_element(By.CSS_SELECTOR, "body")
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    return


#! 내 방 네트워크 환경에서 맥북 에어를 이용하여 합정 5페이지 크롤링에 걸린 시간: 12분
def naver_crawler(area_kor, place_type_kor="가볼만한곳"):

    start_time = time.time()  # !현재 시각

    #! chrome_crawler 설정
    chrome_options = Options()  # !브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  #! 불필요한 에러 메세지 삭제
    service = Service(executable_path=ChromeDriverManager().install())  #! 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service=service, options=chrome_options)
    # main_url = f"https://map.naver.com/v5/search/{area_kor}%20{place_type_kor}/place"
    main_url = f'https://map.naver.com/p/search/{area_kor}%20{place_type_kor}?c=13.00,0,0,0,dh'

    # ! 크롤링할 url로 이동
    crawler.get(main_url)  # ! 웹페이지 해당 주소 이동
    time.sleep(5)  # ! 로딩이 끝날동안 기다리기
    print('페이지 로딩 완료')

    # ! 크롤링한 상점들의 정보를 담는 리스트
    crawl_data = []

    # ? 실제 클릭할 페이지: range(1,6) - 5페이지 / 테스트: range(1,2)
    for page in range(1, 2):
        # ! default 창으로 빠져 나오기
        crawler.switch_to.default_content()
        # ! 프레임 이동
        searchIframe = crawler.find_element(By.ID, "searchIframe")
        crawler.switch_to.frame(searchIframe)
        crawler.implicitly_wait(2)  #! 로딩이 끝날동안 기다리기

        # ! page 클릭하여 이동
        crawler.find_element(By.CSS_SELECTOR,f"#app-root > div > div.XUrfU > div.zRM9F > a:nth-child({page})").click()
        print(f'페이지 이동 to {page}')

        # ! 스크롤 가능하도록 body 중 아무 동작 없는 곳 클릭
        try:
            try:
                crawler.find_element(By.CLASS_NAME, "CHC5F").click() #! 식당,카페,술집
            except:
                try:
                    #_pcmap_list_scroll_container > ul > li:nth-child(2) > div.qbGlu > div.ouxiq.icT4K
                    crawler.find_element(By.CLASS_NAME, "ouxiq.icT4K").click() #! 만화카페
                except:
                    crawler.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.Np1CD > div:nth-child(2)").click() #! 애견카페
            print('스크롤 위해 빈 곳 클릭 완료')
        except:
            pass
        crawler.implicitly_wait(2)

        # ? 페이지의 맨 밑까지 스크롤
        scroll_down(crawler)

        # ! shop들의 목록이 들어있는 className 찾기
        shops = crawler.find_elements(By.CLASS_NAME, "UEzoS.rTjJo") #! 식당,카페,술집
        if len(shops) == 0:
            shops = crawler.find_elements(By.CLASS_NAME, "VLTHu.OW9LQ") #! 만화카페, 전시회, 공원, 스파, 쇼핑몰, 영화관, 원데이클래스, 오락실, 노래방, 볼링장, 뮤지컬, 연극, 콘서트,
        if len(shops) == 0:
            shops = crawler.find_elements(By.CLASS_NAME, "Ki6eC.YPAJV") #! 애견카페, 고양이카페, 보드게임카페, 방탈출카페, 놀이공원, 동뮬원, 수목원/식물원, 스케이트장, 아쿠아리움, 스크린 야구, 

        print(f'총 {len(shops)}개의 장소 찾음')


        # ! 가게들 정보 크롤링 시작
        for shop in shops:
            name, type, star_rating, review_sum, address, contact = NULL, NULL, NULL, NULL, NULL, NULL
            # time_info = NULL

            #! default 콘텐츠로 이동: frame 밖으로 나가기
            crawler.switch_to.default_content()
            #! searchIframe 찾아 들어오기
            searchIframe = crawler.find_element(By.ID, "searchIframe")
            crawler.switch_to.frame(searchIframe)
            crawler.implicitly_wait(2)

            #! 가게 명
            try:
                # name = shop.find_element(By.CLASS_NAME, "place_bluelink.TYaxT").text
                name = shop.find_element(By.CLASS_NAME, "place_bluelink").text #! 모든 검색명 동일
            except:
                name = NULL
            print(f'가게명: {name}')
            crawler.implicitly_wait(2)

            #! 가게 종류
            try:
                try:
                    type = shop.find_element(By.CLASS_NAME, "KCMnt").text #! 식당,카페,술집
                except:
                    try:
                        type = shop.find_element(By.CLASS_NAME, "YzBgS").text #! 만화카페
                    except:
                        type = shop.find_element(By.CLASS_NAME, "wNotu").text #! 애견카페
            except:
                type = NULL
            print(f'종류: {type}')
            crawler.implicitly_wait(2)

            #! 가게명 클릭하여 세부창 띄우기
            try:
                shop.find_element(By.CLASS_NAME, "N_KDL").click() #! 식당,카페,술집
            except:
                try:
                    shop.find_element(By.CLASS_NAME, "C6RjW").click() #! 만화카페
                except:
                    shop.find_element(By.CLASS_NAME, "YFsgn").click() #! 애견카페
            # crawler.implicitly_wait(2)

            #! frame 밖으로 나가기
            crawler.switch_to.default_content()
            #! entryIframe 찾아 들어오기
            entryIframe = crawler.find_element(By.ID, "entryIframe")
            crawler.switch_to.frame(entryIframe)
            crawler.implicitly_wait(2)
            # time.sleep(2)

            #! 영업시간 펼쳐보기 클릭 먼저 해놓기!
            # try:
            #     crawler.find_element(By.CLASS_NAME, "gKP9i.RMgN0").click()
            # except:
            #     print(f"{name}의 영업시간 펼쳐보기 클릭 실패")

            #! 가게 별점
            try:
                star_rating = crawler.find_element(By.CSS_SELECTOR,"#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span.PXMot.LXIwF > em").text #! 모든 검색명 동일
                # star_rating = crawler.find_element(By.CSS_SELECTOR,"span.PXMot.LXIwF > em").text
            except:
                star_rating = NULL
            crawler.implicitly_wait(2)

            #! 방문자리뷰 + 블로그리뷰수
            try:
                review_sum = 0
                reviews = crawler.find_elements(By.CSS_SELECTOR,"#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span > a > em") #! 모든 검색명 동일
                # reviews = crawler.find_elements(By.CSS_SELECTOR,"div.dAsGb > span > a > em")
                for review in reviews:
                    review_sum += int(review.text)
            except:
                review_sum = NULL
            print(f'리뷰수: {review_sum}')
            crawler.implicitly_wait(2)
            time.sleep(0.5)

            #! 가게 주소
            try:
                address = crawler.find_element(By.CLASS_NAME, "LDgIH").text #! 모든 검색명 동일
            except:
                address = NULL
            print(f'주소: {address}')
            crawler.implicitly_wait(2)

            # ? 가게 연락처
            try:
                contact = crawler.find_element(By.CLASS_NAME, "xlx7Q").text #! 모든 검색명 동일
            except:
                contact = NULL
            print(f'연락처: {contact}')


            try:
                url = crawler.find_element(By.ID, 'og:url').get_attribute('content')
            except:
                url = NULL
            print(f'url: {url}')

            try:
                url2 = entryIframe.get_attribute('src')
            except:
                url2 = NULL
            print(f'url2: {url2}')

            keys = [
                "name",
                "type",
                "star_rating",
                "review_sum",
                "address",
                "contact",
                "url"
            ]
            values = [name, type, star_rating, review_sum, address, contact, url]
            crawl_data.append(dict(zip(keys, values)))

    end_time = time.time()  #! 끝난 시간
    print(f"크롤링에 걸린 시간: {(int(end_time - start_time)//60)}분 {(int(end_time - start_time))%60}초")

    crawler.quit()
    print(f'크롤링 끝')

    for data in crawl_data:
        print(data)

    with open(f"data_process/csv/{area_kor_to_eng[area_kor]}_{type_searchname_to_typecode[place_type_kor]}.csv", "w", encoding="UTF-8") as file:
        csvWriter = csv.DictWriter(file, fieldnames=keys)
        csvWriter.writeheader()
        csvWriter.writerows(crawl_data)
    
    print(f'{area_kor}_{place_type_kor} 크롤링하여 데이터 저장 성공')
