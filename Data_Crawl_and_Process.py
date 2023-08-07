from Crawler.naver_crawler import naver_crawler
from FileTransform.fileTransform import csv_to_excel
from DataProcessing.dataProcesing import processed_data_to_csv
from constant import area_kor_to_eng, type_kor_to_eng
from datetime import datetime

#? 데이터 크롤링하여 csv파일과 엑셀파일로 저장
class Data_Crawl_and_Process:
    def __init__(self):
        self.today = datetime.today()
        print(f'오늘 날짜: {self.today.strftime("%Y-%m-%d")}')
    
    def all(self):
        for area in area_kor_to_eng.keys():
            for place_type in type_kor_to_eng.keys():
                #? 크롤링 -> 저장
                try:
                    naver_crawler(area, place_type)
                    csv_to_excel(f"./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}.csv", 
                                 f"./excel/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}.xlsx")  #? 엑셀에 데이터 저장

                    print(f'{area} 크롤링 성공')
                except:
                    print(f'{area} 크롤링 실패')
                #? 데이터 처리
                try:
                    processed_data_to_csv(area_kor_to_eng[area], 
                                          f'./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}.csv', 
                                          f'./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}_processed.csv')
                    csv_to_excel(f"./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}_processed.csv", 
                                 f"./excel/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}_processed.xlsx")
                    print(f'{area} 데이터처리 성공')
                except:
                    print(f'{area} 데이터처리 실패')
        return
    
    def one(self, area, place_type):
        try:
            naver_crawler(area, place_type)
            csv_to_excel(f"./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}.csv", 
                         f"./excel/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}.xlsx")  #? 엑셀에 데이터 저장
            print(f'{area} 크롤링 성공')
        except:
            print(f'{area} 크롤링 실패')
    
        try:
            processed_data_to_csv(area_kor_to_eng[area], 
                                  f'./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}.csv', 
                                  f'./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}_processed.csv')
            csv_to_excel(f"./csv/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}_processed.csv", 
                         f"./excel/{area_kor_to_eng[area]}_{type_kor_to_eng[place_type]}_processed.xlsx")
            print(f'{area} 데이터처리 성공')
        except:
            print(f'{area} 데이터처리 실패')
        return