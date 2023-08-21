from ..constant import area_kor_to_eng, type_searchname_to_typecode
from .fileTransform import csv_to_xlsx
from .naverCrawler import naver_crawler
from .dataProcesor import processed_data_to_csv
from datetime import datetime

#! 데이터 크롤링하여 csv파일과 엑셀파일로 저장
class Data_Crawl_and_Process:
    def __init__(self):
        self.today = datetime.today()
        self.fail = []
        print(f'오늘 날짜: {self.today.strftime("%Y-%m-%d")}')
        
    def get_one(self, area_kor, type_kor):
        area_eng = area_kor_to_eng[area_kor]
        type_code = type_searchname_to_typecode[type_kor]
        try:
            naver_crawler(area_kor, type_kor)
            csv_to_xlsx(f"data_process/csv/{area_eng}_{type_code}.csv", f"data_process/xlsx/{area_eng}_{type_code}.xlsx") 
            print(f'{area_kor}_{type_kor} 크롤링하여 데이터 저장 성공')
        except:
            print(f'{area_kor}_{type_kor} 크롤링/데이터저장 실패')
    
        try:
            processed_data_to_csv(area_eng, type_code,
                                f'data_process/csv/{area_eng}_{type_code}.csv', 
                                f'data_process/csv/{area_eng}_{type_code}_processed.csv')
            print('(중간) processed_data_to_csv 완료')
            csv_to_xlsx(f"data_process/csv/{area_eng}_{type_code}_processed.csv", f"data_process/xlsx/{area_eng}_{type_code}_processed.xlsx")
            print(f'{area_kor}_{type_kor} 데이터 가공하여 저장 성공')
        except:
            print(f'{area_kor}_{type_kor} 데이터 가공/저장 실패')
        return
    
    
    def get_one_area(self, area_kor):
        for type_kor, type_code in type_searchname_to_typecode.items():
            self.get_one(area_kor,type_kor)
        return


    def get_all_area(self):
        for area_kor, area_eng in area_kor_to_eng.items():
            self.get_one_area(area_kor)
        return