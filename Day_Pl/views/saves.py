from django.shortcuts import render, redirect
from ..models import Place, PlaceType, Plan, PlanPlace, Preference, UserPlanView

def index(request):
    user = request.user

    plans_places = []
    check_planid = []

    #! 내가 좋아하는 플랜들
    print('<좋아요 누른 플랜들>')
    like_plans = user.plans.all()
    print(like_plans)
    for like_plan in like_plans:
        print(f'plan_title: {like_plan.title} plan_id: {like_plan.id} 하트수: {like_plan.like_users.count()}')
        like_plan_places = PlanPlace.objects.filter(plan = like_plan).order_by('order')
        #! 중복처리
        if like_plan.id not in check_planid:
            plans_places.append(like_plan_places)
            check_planid.append(like_plan.id)

    print()

    #! 내가 본 플랜들
    print('<봤던 플랜들>')
    saw_plans = user.plans_view.all()
    for saw_plan in saw_plans:
        print(f'plan_title: {saw_plan.title} plan_id: {saw_plan.id} 하트수: {saw_plan.like_users.count()}')
        saw_plan_places = PlanPlace.objects.filter(plan = saw_plan).order_by('order')
        #! 중복처리
        if saw_plan.id not in check_planid:
            plans_places.append(saw_plan_places)
            check_planid.append(saw_plan.id)

    for plan_places in plans_places:
        for i in range(len(plan_places)-1):
            road_url = f"https://map.naver.com/p/directions/,,,{ plan_places[i].place.naver_place_id },PLACE_POI/,,,{ plan_places[i+1].place.naver_place_id },PLACE_POI/-/transit?c=13.00,0,0,0,dh"
            PlanPlace.objects.filter(id = plan_places[i].id).update(road_url=road_url)

    context = {
        'like_plans': like_plans,
        'saw_plans': saw_plans,
        'plans_places': plans_places
    }
    return render(request, 'saves.html', context=context)