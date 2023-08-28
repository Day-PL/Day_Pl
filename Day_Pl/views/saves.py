<<<<<<< HEAD
from django.shortcuts import render
from ..models import  PlanPlace 
=======
from django.shortcuts import render, redirect
from ..models import Place, PlaceType, Plan, PlanPlace, Preference, UserPlanView
>>>>>>> 138dfd0 (rename : 사용 안하는 import 삭제 및 db 변경)

def index(request):
    user = request.user

    plans_places = []
    check_planid = []

    #! 내가 좋아하는 플랜들
    like_plans = user.like_plans.all()
    for like_plan in like_plans:
        like_plan_places = PlanPlace.objects.filter(plan = like_plan).order_by('order')
        #! 중복처리
        if like_plan.id not in check_planid:
            plans_places.append(like_plan_places)
            check_planid.append(like_plan.id)

    #! 내가 본 플랜들
    view_plans = user.view_plans.all()
    for view_plan in view_plans:
        view_plan_places = PlanPlace.objects.filter(plan = view_plan).order_by('order')
        #! 중복처리
        if view_plan.id not in check_planid:
            plans_places.append(view_plan_places)
            check_planid.append(view_plan.id)
    
    # TODO new_plan으로 가야 할 것 같다
    for plan_places in plans_places:
        for i in range(len(plan_places)-1):
            road_url = f"https://map.naver.com/p/directions/,,,{ plan_places[i].place.naver_place_id },PLACE_POI/,,,{ plan_places[i+1].place.naver_place_id },PLACE_POI/-/transit?c=13.00,0,0,0,dh"
            PlanPlace.objects.filter(id = plan_places[i].id).update(road_url=road_url)

    context = {
        'like_plans': like_plans,
        'view_plans': view_plans,
        'plans_places': plans_places
    }
    return render(request, 'saves.html', context=context)