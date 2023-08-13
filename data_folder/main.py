from d_crawl_to_process import Data_Crawl_and_Process

if __name__ == "__main__":
    machine = Data_Crawl_and_Process()

    machine.get_all_area()              #! 모든 지역 + 모든 종류 데이터 가져오기
    # machine.get_one_area('익선동')        #! 익선동 데이터만 가져오기
    # machine.get_one('익선동', '만화카페')   #! 익선동 + 만화카페 데이터만 가져오기 -> 
    # machine.get_one('익선동', '전시회')     #! 익선동 + 전시회 데이터만 가져오기 -> 익선동이 아니라 종로/서울로 지역 변경하면 좀 더 좋을 것 같다.
    # machine.get_one('종로', '애견카페')     #! 익선동 + 애견카페 데이터만 가져오기 -> 익선동이 아니라 서울 이라고 검색해야한다!
    # machine.get_one('익선동', '고양이카페')  #! 익선동 + 애견카페 데이터만 가져오기 -> 위와 동일
    # machine.get_one('익선동', '원데이클래스') #! 익선동 + 원데이클래스 데이터만 가져오기 -> 위와 동일
    print(f'실패한 항목: {machine.fail}')