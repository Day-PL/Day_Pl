import csv
from datetime import datetime
from a_constant import NULL


def processed_data_to_csv(area_Eng, before_file, after_file):
    processed_data = []
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #? csv 파일 불러와서 영업시간 데이터 전처리
    with open(before_file, "r", encoding="UTF-8") as file:
        csvReader = csv.DictReader(file)
        for shop in csvReader:
            name = shop["name"]
            type = shop["type"]
            star_rating = shop["star_rating"]
            review_sum = shop["review_sum"]
            address = shop["address"]
            # open_info = shop["time_info"]
            contact = shop["contact"]

            # if star_rating == NULL:
            #     star_rating = 0.0

            # open_info_by_day = {
            #     "월": {"opening_hours": NULL, "last_order_time": NULL},
            #     "화": {"opening_hours": NULL, "last_order_time": NULL},
            #     "수": {"opening_hours": NULL, "last_order_time": NULL},
            #     "목": {"opening_hours": NULL, "last_order_time": NULL},
            #     "금": {"opening_hours": NULL, "last_order_time": NULL},
            #     "토": {"opening_hours": NULL, "last_order_time": NULL},
            #     "일": {"opening_hours": NULL, "last_order_time": NULL},
            # }
            # open_info = open_info.replace("'", "").strip("[[").strip("]]").split("], [")

            # for day in open_info[1:]:  #? 0번째는 현재 영업중 정보
            #     day = day.split(", ")
            #     if len(day) >= 3:
            #         yoil, time_info, last_order = day[0], day[1], day[2]
            #     elif len(day) >= 2:
            #         yoil, time_info, last_order = day[0], day[1], NULL
            #     elif len(day) == 1:
            #         yoil, time_info, last_order = day[0], NULL, NULL
            #     else:
            #         yoil, time_info, last_order = NULL, NULL, NULL

            #     if "휴무" in time_info:
            #         time_info = "휴무"
            #     elif "-" in time_info and "/" not in time_info:
            #         i = time_info.index("-")
            #         open_time, close_time = (
            #             time_info[i - 6 : i - 1],
            #             time_info[i + 2 : i + 7],
            #         )
            #         open_hour, open_minute = int(open_time[:2]), int(open_time[3:])
            #         close_hour, close_minute = int(close_time[:2]), int(close_time[3:])
            #         if open_hour > close_hour:
            #             close_hour += 24
            #         time_info = f"{open_hour:02d}:{open_minute:02d}-{close_hour:02d}:{close_minute:02d}"

            #     if "라스트오더" in last_order:
            #         if "시" in last_order:
            #             if "분" in last_order:  #? (ex.21시 30분에 라스트오더)
            #                 last_order = f"{int(last_order.split('시', '분')[0]):02d}:{int(last_order.split('시', '분')[1]):02d}"
            #             else:  #  (ex.21시에 라스트 오더/ 이건 있는 경우인지 모르겠다)
            #                 last_order = f"{int(last_order.split('시')[0]):02d}:00"
            #         else:  #? (ex.23:00 라스트오더)
            #             last_order = last_order.split(" ")[0]

            #     try:
            #         if yoil in ["매일"]:
            #             #? 모든 요일 처리
            #             for key in open_info_by_day.keys():
            #                 open_info_by_day[key] = {
            #                     "opening_hours": time_info,
            #                     "last_order_time": last_order,
            #                 }
            #         elif yoil[0] in ["월", "화", "수", "목", "금", "토", "일"]:
            #             open_info_by_day[yoil] = {
            #                 "opening_hours": time_info,
            #                 "last_order_time": last_order,
            #             }
            #     except:
            #         pass

            keys = [
                "create_time",
                "area",
                "name",
                "type",
                "star_rating",
                "review_sum",
                "address",
                # "mon_opening_hours",
                # "mon_last_order_time",
                # "tue_opening_hours",
                # "tue_last_order_time",
                # "wed_opening_hours",
                # "wed_last_order_time",
                # "thu_opening_hours",
                # "thu_last_order_time",
                # "fri_opening_hours",
                # "fri_last_order_time",
                # "sat_opening_hours",
                # "sat_last_order_time",
                # "sun_opening_hours",
                # "sun_last_order_time",
                "contact",
            ]

            values = [
                create_time,
                area_Eng,
                name,
                type,
                star_rating,
                review_sum,
                address,
                # open_info_by_day["월"]["opening_hours"],
                # open_info_by_day["월"]["last_order_time"],
                # open_info_by_day["화"]["opening_hours"],
                # open_info_by_day["화"]["last_order_time"],
                # open_info_by_day["수"]["opening_hours"],
                # open_info_by_day["수"]["last_order_time"],
                # open_info_by_day["목"]["opening_hours"],
                # open_info_by_day["목"]["last_order_time"],
                # open_info_by_day["금"]["opening_hours"],
                # open_info_by_day["금"]["last_order_time"],
                # open_info_by_day["토"]["opening_hours"],
                # open_info_by_day["토"]["last_order_time"],
                # open_info_by_day["일"]["opening_hours"],
                # open_info_by_day["월"]["last_order_time"],
                contact,
            ]
            processed_data.append(dict(zip(keys, values)))

    # ? csv 파일에 저장
    with open(after_file, "w", encoding="UTF-8") as file:
        csvWriter = csv.DictWriter(file, fieldnames=keys)
        csvWriter.writeheader()
        for row in processed_data:
            csvWriter.writerow(row)

    print(f"{after_file} 생성이 완료되었습니다.")
