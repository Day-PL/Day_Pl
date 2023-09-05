from django.shortcuts import render, redirect, HttpResponse
from ..models import Plan, PlanPlace 


def index(request):
    user = request.user

    plans_places = []
    check_planid = []

    #! 내가 좋아하는 플랜들
    like_plans = user.like_plans.all()
    for plan in like_plans:
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)

    #! 내가 본 플랜들
    view_plans = user.view_plans.all()
    for plan in view_plans:
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)
    
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

def remove(request, plan_id):
    user = request.user
    plan = user.like_plans.get(id=plan_id)
    plan.like_users.remove(user)
    return HttpResponse('Success', status = 200)

def add(request, plan_id):
    user = request.user
    plan = Plan.objects.get(id=plan_id)
    plan.like_users.add(user)
    return HttpResponse('Success', status = 200)