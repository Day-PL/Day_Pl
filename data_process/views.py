from django.shortcuts import render, redirect
from .crawler.fileTransform import naver_place_csv_to_db
from .constant import area_kor_to_eng, type_searchname_to_typecode
from .crawler.crawl_to_process import Data_Crawl_and_Process
from .exhibit_crawler.interpark_crawler import interpark_crawler
from .exhibit_crawler.data_save_to import save_to_db
from .api.naver_api_test import naver_api_search_info
from Day_Pl.models import Place


def naver_place_crawler(request):
    machine = Data_Crawl_and_Process()
    machine.get_all_area()               #! 모든 지역 + 모든 종류 데이터 가져오기
    # machine.get_one('종로', '식당')        #! 종로 식당 데이터만 가져오기
    print(f'실패한 항목: {machine.fail}')
    return redirect('Day_Pl:browse')

def naver_place_csv_to_db_all(request):
    for area_kor in area_kor_to_eng:
        for typecode in type_searchname_to_typecode.values():
            try:
                naver_place_csv_to_db(area_kor, typecode)
            except:
                pass
    return render(request, 'browse.html')

def exhibit_crawler(request):
    interpark_crawler()
    return redirect('Day_Pl:browse')

def exhibit_save_to_db(request, date):
    save_to_db(f'data_process/exhibit_crawler/interpark_csv/exhibit_{date}.csv')
    return redirect('Day_Pl:browse')
    return redirect('Day_Pl:browse')

def naver_api_search(request):
    naver_api_search_info()
    return redirect('Day_Pl:browse')

def place_obj_create(request):
    Place.objects.create(id=0, name='', address_si='', address_gu='', address_lo='') #! type_code
    print(Place.objects.filter(id=0))
    return redirect('Day_Pl:browse')