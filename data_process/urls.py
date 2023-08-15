from django.urls import path
from .views import naver_place_crawler, naver_place_csv_to_db_all

app_name = "data_process"

urlpatterns = [
    path("naver_place_crawler/",       naver_place_crawler,       name = 'naver_place_crawler'), 
    path("naver_place_csv_to_db_all/", naver_place_csv_to_db_all, name = 'naver_place_csv_to_db_all'),

]