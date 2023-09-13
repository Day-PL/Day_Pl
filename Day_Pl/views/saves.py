from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from ..models import Plan, PlanPlace , Place, PlaceType, PlaceTypeCategory
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse
import json
from datetime import date, datetime
from django.db import transaction


def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('common:login'))
    
    login_user = request.user
    like_plans = login_user.like_plans.all()
    view_plans = login_user.view_plans.all()
    my_plans   = Plan.objects.filter(user=login_user)

    like_plans_processed, view_plans_processed, my_plans_processed = [], [], []
    plans_places, check_planid = [], []

    #! 내가 좋아하는 플랜들
    for plan in like_plans:
        plan_dict = {
            'create_user': plan.user,
            'id'         : plan.id,
            'uuid'       : plan.uuid,
            'title'      : plan.title,
            'created_at' : plan.created_at,
            'modified_at'  : plan.modified_at,
            'hashtag_area' : plan.hashtag_area,
            'hashtag_type' : plan.hashtag_type,
            'hashtag_pick' : plan.hashtag_pick,
            'memo'       : plan.memo,
            'total_time' : plan.total_time,
            'public'     : plan.public,
            'like_count' : plan.like_users.count(),
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
            'create_user': plan.user,
            'id'         : plan.id,
            'uuid'       : plan.uuid,
            'title'      : plan.title,
            'created_at' : plan.created_at,
            'modified_at'  : plan.modified_at,
            'hashtag_area' : plan.hashtag_area,
            'hashtag_type' : plan.hashtag_type,
            'hashtag_pick' : plan.hashtag_pick,
            'memo'       : plan.memo,
            'total_time' : plan.total_time,
            'public'     : plan.public,
            'like_count' : plan.like_users.count(),
        }
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)
        #! 내가 좋아하는 것인지 판별
        if login_user.like_plans.filter(id=plan.id).exists():
            plan_dict['islike'] = True
        else:
            plan_dict['islike'] = False
        view_plans_processed.append(plan_dict)
        
    
    for plan in my_plans:
        plan_dict = {
            'create_user': plan.user,
            'id'         : plan.id,
            'uuid'       : plan.uuid,
            'title'      : plan.title,
            'created_at' : plan.created_at,
            'modified_at'  : plan.modified_at,
            'hashtag_area' : plan.hashtag_area,
            'hashtag_type' : plan.hashtag_type,
            'hashtag_pick' : plan.hashtag_pick,
            'memo'       : plan.memo,
            'total_time' : plan.total_time,
            'public'     : plan.public,
            'like_count' : plan.like_users.count(),
        }
        plan_places = PlanPlace.objects.filter(plan = plan).order_by('order')
        #! 중복처리
        if plan.id not in check_planid:
            plans_places.append(plan_places)
            check_planid.append(plan.id)
        if login_user.like_plans.filter(id=plan.id).exists():
            plan_dict['islike'] = True
        else:
            plan_dict['islike'] = False
        my_plans_processed.append(plan_dict)


    context = {
        'plans_places'        : plans_places,
        'like_plans_processed': like_plans_processed,
        'view_plans_processed': view_plans_processed,
        'my_plans_processed'  : my_plans_processed,
    }
    return render(request, 'saves.html', context=context)


def remove_likeplan(request, plan_id):
    login_user = request.user
    plan = login_user.like_plans.get(id=plan_id)
    plan.like_users.remove(login_user)
    return HttpResponse('Success', status = 200)


def add_likeplan(request, plan_id):
    login_user = request.user
    plan = Plan.objects.get(id=plan_id)
    plan.like_users.add(login_user)
    return HttpResponse('Success', status = 200)

def remove_plan(request, plan_id):
    login_user = request.user
    plan = Plan.objects.get(id=plan_id)
    print(f'{plan.title} 삭제')
    plan.delete()
    return HttpResponseRedirect(reverse('Day_Pl:saves'))


def modify_plan(request, plan_id):
    login_user = request.user
    plan_before = get_object_or_404(Plan, id = plan_id)
    print(f'{plan_before.title} 수정')
    plan_places = PlanPlace.objects.filter(plan = plan_before).order_by('order')
    places = Place.objects.all()[1:]
    placetypes = PlaceType.objects.all()
    placetype_categories = PlaceTypeCategory.objects.all()
    current_date = date.today()

    if not request.user.is_authenticated:
        return redirect(reverse('common:login'))
    
    if request.method == "GET":
        if plan_before:
            plan_places_before = PlanPlace.objects.filter(plan=plan_before).order_by('order')

            plan_places = []
            for plan_place in plan_places_before:
                isuserlike_place = plan_place.place.like_users.filter(id=request.user.id).exists()
                plan_places.append({
                                    'place': plan_place.place,
                                    'isuserlike_place': isuserlike_place,
                                    })
            plan = {
                'title' : plan_before.title,
                'isuserlike_plan': plan_before.like_users.filter(id=request.user.id).exists(),
                'hashtags' : f'{plan_before.hashtag_area}, {plan_before.hashtag_pick}, {plan_before.hashtag_type}'
            }

    elif request.method == "POST":
        data         = json.loads(request.body)

        title        = data.get('plantitle')
        place_ids    = data.get('placeids')
        is_liked     = data.get('isliked')
        hashtag_area = data.get('hashtag_area')
        hashtag_type = data.get('hashtag_type')
        hashtag_pick = data.get('hashtag_pick')
        is_public    = data.get('ispublic')

        with transaction.atomic():
            try:
                plan_before.title        = title
                plan_before.hashtag_area = hashtag_area
                plan_before.hashtag_type = hashtag_type
                plan_before.hashtag_pick = hashtag_pick
                plan_before.public       = is_public
                if is_liked:
                    plan_before.like_users.add(login_user)
                plan_before.save()
                print(place_ids)
                PlanPlace.objects.filter(plan = plan_before).all().delete()
                for idx, place_id in enumerate(place_ids):
                    place_obj = Place.objects.get(id = place_id)
                    PlanPlace.objects.create(
                                                plan = plan_before,
                                                place = place_obj,
                                                order = idx,
                                            )
                print('추가')
                plan_places = PlanPlace.objects.filter(plan = plan_before).order_by('order')
                for i in range(len(plan_places)-1):
                    road_url = f"https://map.naver.com/p/directions/,,,{ plan_places[i].place.naver_place_id },PLACE_POI/,,,{ plan_places[i+1].place.naver_place_id },PLACE_POI/-/walk?c=13.00,0,0,0,dh"
                    print(road_url)
                    PlanPlace.objects.filter(id = plan_places[i].id).update(road_url=road_url)
                response = {
                    'status': 'success',
                }
            except Exception:
                # 로그
                transaction.set_rollback(True)
                response = {
                    'status': 'fail',
                }
        return JsonResponse(response)

    context = {
        'plan' : plan,
        'plan_places' : plan_places,
        'placetype_categories' : placetype_categories,
    }
    return render(request, 'modify_plan.html', context=context)
