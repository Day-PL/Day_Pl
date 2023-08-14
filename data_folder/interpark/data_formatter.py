from datetime import datetime

def format_date(str_date):
    str_start_date = str_date[:10]
    str_end_date = str_date[-10:]
    start_date = datetime.strptime(str_start_date, "%Y.%m.%d").strftime('%Y-%m-%d')
    end_date = datetime.strptime(str_end_date, "%Y.%m.%d").strftime('%Y-%m-%d')
    return start_date, end_date
