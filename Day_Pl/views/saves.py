from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from ..models import Plan, PlanPlace 
from django.core import serializers
from django.urls import reverse
import json


def index(request):
    user = request.user
    like_plans = user.like_plans.all()
    view_plans = user.view_plans.all()
    my_plans   = Plan.objects.filter(user=user)

    like_plans_processed, view_plans_processed, my_plans_processed = [], [], []
    plans_places, check_planid = [], []

    #! 내가 좋아하는 플랜들
    for plan in like_plans:
        plan_dict = {
            'id' : plan.id,
            'uuid' : plan.uuid,
            'title' : plan.title,
            'like_count' : plan.like_users.count(),
            'public' : plan.public,
        }
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)
        like_plans_processed.append(plan_dict)

    #! 내가 본 플랜들
    for plan in view_plans:
        plan_dict = {
            'id' : plan.id,
            'uuid' : plan.uuid,
            'title' : plan.title,
            'like_count' : plan.like_users.count(),
            'public' : plan.public,
        }
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)
        #! 내가 좋아하는 것인지 판별
        # if plan.like_users.filter(id=user.id).exists():
        if user.like_plans.filter(id=plan.id).exists():
            plan_dict['islike'] = True
        else:
            plan_dict['islike'] = False
        view_plans_processed.append(plan_dict)
        
    
    for plan in my_plans:
        plan_dict = {
            'id' : plan.id,
            'uuid' : plan.uuid,
            'title' : plan.title,
            'like_count' : plan.like_users.count(),
            'public' : plan.public,
        }
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)
        if user.like_plans.filter(id=plan.id).exists():
            plan_dict['islike'] = True
        else:
            plan_dict['islike'] = False
        my_plans_processed.append(plan_dict)
    
    # TODO : new_plan으로 가야 할 것 같다
    for plan_places in plans_places:
        for i in range(len(plan_places)-1):
            road_url = f"https://map.naver.com/p/directions/,,,{ plan_places[i].place.naver_place_id },PLACE_POI/,,,{ plan_places[i+1].place.naver_place_id },PLACE_POI/-/transit?c=13.00,0,0,0,dh"
            PlanPlace.objects.filter(id = plan_places[i].id).update(road_url=road_url)

    context = {
        'plans_places': plans_places,
        'like_plans_processed': like_plans_processed,
        'view_plans_processed': view_plans_processed,
        'my_plans_processed': my_plans_processed,
    }
    return render(request, 'saves.html', context=context)


def remove_likeplan(request, plan_id):
    user = request.user
    plan = user.like_plans.get(id=plan_id)
    plan.like_users.remove(user)
    return HttpResponse('Success', status = 200)


def add_likeplan(request, plan_id):
    user = request.user
    plan = Plan.objects.get(id=plan_id)
    plan.like_users.add(user)
    return HttpResponse('Success', status = 200)

def remove_plan(request, plan_id):
    user = request.user
    plan = Plan.objects.get(id=plan_id)
    print(f'{plan.title} 삭제')
    plan.delete()
    return HttpResponseRedirect(reverse('Day_Pl:saves'))

def modify_plan(request, plan_id):
    user = request.user
    plan = Plan.objects.get(id=plan_id)
    print(f'{plan.title} 수정')
    places = PlanPlace.objects.filter(plan = plan).order_by('order')
    plan_dict = {
            'id' : plan.id,
            'uuid' : plan.uuid,
            'title' : plan.title,
            'like_count' : plan.like_users.count(),
            'public' : plan.public,
            'places' : places,
    }
    return HttpResponseRedirect(reverse('Day_Pl:browse'))
