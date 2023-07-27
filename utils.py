# 출처: https://www.seoul.go.kr/seoul/autonomy_sub.do

SECRET_KEY = "2023_Day'Pl"


area_dict = {
    '강남구': ['신사동', '압구정', '청담동', '삼성동', '대치동', '역삼동', '도곡동'],
    '강동구': ['천호동', '길동'],
    '강북구': ['미아동', '수유동', '우이동'],
    '강서구': ['염창동', '등촌동','발산동'],
    '마포구': ['망원', '상암동', '서교동', '아현동', '연남동', '합정', '홍대'],
    '서대문구':['신촌', '연희동', '가좌동']
    }

# ㄱㄴㄷ 순 / 구 제외하고 동만!
kor_to_eng = {
    '망원동': 'mangwondong',
    '신사동':'sinsadong',
    '연남동': 'yeonnamdong',
    '연희동': 'yeonhuidong',
    '역삼동': 'yeoksamdong',
    '합정동': 'hapjeongdong',
    }