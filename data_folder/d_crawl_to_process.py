from a_constant import area_kor_to_eng, type_searchname_to_typecode
from a_fileTransform import csv_to_xlsx
from b_naverCrawler import naver_crawler
from c_dataProcesor import processed_data_to_csv
from datetime import datetime

#? 데이터 크롤링하여 csv파일과 엑셀파일로 저장
class Data_Crawl_and_Process:
    def __init__(self):
        self.today = datetime.today()
        self.fail = []
        print(f'오늘 날짜: {self.today.strftime("%Y-%m-%d")}')
        
    
    def get_all_area(self):
        for area_kor, area_eng in area_kor_to_eng.items():
            if area_eng == "":
                continue
            for place_type_kor, place_type_eng in type_searchname_to_typecode.items():
                try:
                    #! 크롤링하여 csv로 저장
                    naver_crawler(area_kor, place_type_kor)
                    #! 엑셀로 저장
                    csv_to_xlsx(f"./csv/{area_eng}_{place_type_eng}.csv", 
                                 f"./xlsx/{area_eng}_{place_type_eng}.xlsx") 

                    print(f'{area_kor}_{place_type_kor} 크롤링하여 데이터 저장 성공')
                except:
                    print(f'{area_kor}_{place_type_kor} 크롤링/데이터저장 실패')
                    self.fail.append(f'{area_kor}_{place_type_kor}')
                
                try:
                    #! 데이터 처리하여 csv로 저장
                    processed_data_to_csv(area_eng, 
                                          f'./csv/{area_eng}_{place_type_eng}.csv', 
                                          f'./csv/{area_eng}_{place_type_eng}_processed.csv')
                    #! 엑셀로 저장
                    csv_to_xlsx(f"./csv/{area_eng}_{place_type_eng}_processed.csv", 
                                 f"./xlsx/{area_eng}_{place_type_eng}_processed.xlsx")
                    print(f'{area_kor}_{place_type_kor} 데이터 가공하여 저장 성공')
                except:
                    print(f'{area_kor}_{place_type_kor} 데이터 가공/저장 실패')
        return
    
    def get_one_area(self, area_kor):
        area_eng = area_kor_to_eng[area_kor]
        for place_type_kor, place_type_eng in type_searchname_to_typecode.items():
            try:
                naver_crawler(area_kor, place_type_kor)
                csv_to_xlsx(f"./csv/{area_eng}_{place_type_eng}.csv", 
                            f"./xlsx/{area_eng}_{place_type_eng}.xlsx") 
                print(f'{area_kor}_{place_type_kor} 크롤링하여 데이터 저장 성공')
            except:
                print(f'{area_kor}_{place_type_kor} 크롤링/데이터저장 실패')
        
            try:
                processed_data_to_csv(area_eng, 
                                    f'./csv/{area_eng}_{place_type_eng}.csv', 
                                    f'./csv/{area_eng}_{place_type_eng}_processed.csv')
                csv_to_xlsx(f"./csv/{area_eng}_{place_type_eng}_processed.csv", 
                            f"./xlsx/{area_eng}_{place_type_eng}_processed.xlsx")
                print(f'{area_kor}_{place_type_kor} 데이터 가공하여 저장 성공')
            except:
                print(f'{area_kor}_{place_type_kor} 데이터 가공/저장 실패')
        return

    def get_one(self, area_kor, place_type_kor):
        area_eng = area_kor_to_eng[area_kor]
        place_type_eng = type_searchname_to_typecode[place_type_kor]
        try:
            naver_crawler(area_kor, place_type_kor)
            csv_to_xlsx(f"./csv/{area_eng}_{place_type_eng}.csv", 
                        f"./xlsx/{area_eng}_{place_type_eng}.xlsx") 
            print(f'{area_kor}_{place_type_kor} 크롤링하여 데이터 저장 성공')
        except:
            print(f'{area_kor}_{place_type_kor} 크롤링/데이터저장 실패')
    
        try:
            processed_data_to_csv(area_eng, 
                                f'./csv/{area_eng}_{place_type_eng}.csv', 
                                f'./csv/{area_eng}_{place_type_eng}_processed.csv')
            csv_to_xlsx(f"./csv/{area_eng}_{place_type_eng}_processed.csv", 
                        f"./xlsx/{area_eng}_{place_type_eng}_processed.xlsx")
            print(f'{area_kor}_{place_type_kor} 데이터 가공하여 저장 성공')
        except:
            print(f'{area_kor}_{place_type_kor} 데이터 가공/저장 실패')
        return