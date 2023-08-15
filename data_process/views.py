from django.shortcuts import render
from .crawler.fileTransform import naver_place_csv_to_db
from .constant import area_kor_to_eng, type_searchname_to_typecode
from .crawler.crawl_to_process import Data_Crawl_and_Process


def naver_place_crawler(request):
    machine = Data_Crawl_and_Process()
    machine.get_all_area()               #! 모든 지역 + 모든 종류 데이터 가져오기
    # machine.get_one('종로', '식당')        #! 종로 식당 데이터만 가져오기
    print(f'실패한 항목: {machine.fail}')
    return render(request, 'browse.html')

def naver_place_csv_to_db_all(request):
    for area_kor in area_kor_to_eng:
        for typecode in type_searchname_to_typecode.values():
            try:
                naver_place_csv_to_db(area_kor, typecode)
            except:
                pass
    return render(request, 'browse.html')
