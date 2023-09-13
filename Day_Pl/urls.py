from .views import browse, preferences, saves, new_plan, populars, modify_profile
from .components import check_like
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

app_name = "Day_Pl"

urlpatterns = [
    path("", browse.index, name = 'browse'), #! 메인 페이지
    path("preferences/", preferences.index, name = 'preferences'), #! 선호도 조사 페이지 (회원가입 이후 뜨는 창, 선호도 수정시 가는 창)
    path('modify_profile/', modify_profile.modify_profile, name='modify_profile'),
    path("saves/", saves.index, name = 'saves'),    #! 기록 페이지
    path("saves/<int:plan_id>/like/remove", saves.remove_likeplan, name = 'remove-likeplan'),
    path("saves/<int:plan_id>/like/add",    saves.add_likeplan,    name = 'add-likeplan'),
    path("saves/<int:plan_id>/remove",    saves.remove_plan,    name = 'remove-plan'),
    path("saves/<int:plan_id>/modify",    saves.modify_plan,    name = 'modify-plan'),
    # path("saves/<str:plan_uuid>/", saves.detail, name = 'saves_detail'), #! 기록 페이지 / 플랜 하나
    # path("saves/<str:plan_uuid>/update/", saves.update, name = 'saves_update'), #! 기록 페이지 / 플랜 하나 업데이트
    path("new-plan/", new_plan.index, name='new_plan'), #! 새로운 플랜 짜는 창
    path("get-filter/<int:placetype_id>/<str:search_keyword>/", new_plan.get_filter, name='get_filter'),
    path("new-plan/comment/", new_plan.control_comment, name='control-place-comment'),
    path("new-plan/comment/<int:place_id>/", new_plan.place_comment, name='place-comment'),
    path("check-place-like/<int:place_id>/", check_like.check_place_like, name = 'check-place-like'),
    path("check-plan-like/<int:plan_id>/", check_like.check_plan_like, name = 'check-plan-like'),
    path("new-plan/naver_map/", new_plan.get_naver_map, name='get_naver_map'), 
    path("populars/", populars.index, name='populars'), #! 인기 많은 플랜들 뜨는 창
    path("populars/search/<str:search_keyword>/", populars.get_plans, name='get-plans'),
    path("populars/<str:plan_id>/", populars.detail, name='populars-detail'), #! 인기 많은 플랜들 / 플랜 하나
    path("populars/detail/<str:plan_id>/", populars.share_detail, name='populars-share-detail'), #! 인기 많은 플랜들 / 플랜 하나
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)