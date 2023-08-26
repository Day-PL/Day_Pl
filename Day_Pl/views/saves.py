from django.shortcuts import render, redirect
from ..models import Place, PlaceType, Plan, PlanPlace, Preference, UserPlanView
from django.contrib.auth.models import User
# from common.models import User

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
    saw_plans = UserPlanView.objects.filter(user = user)
    print(saw_plans)
    for saw_plan in saw_plans:
        print(f'plan_title: {saw_plan.plan.title} plan_id: {saw_plan.plan.id} 하트수: {saw_plan.plan.like_users.count()}')
        saw_plan_places = PlanPlace.objects.filter(plan = saw_plan.plan).order_by('order')
        #! 중복처리
        if saw_plan.plan.id not in check_planid:
            plans_places.append(saw_plan_places)
            check_planid.append(saw_plan.plan.id)

    for plan_places in plans_places:
        print(plan_places)
        for plan_place in plan_places:
            print(f'{plan_place.plan.title:15s}, {plan_place.place.name:15s}')

    context = {
        'like_plans': like_plans,
        'saw_plans': saw_plans,
        'plans_places': plans_places
    }
    return render(request, 'saves.html', context=context)