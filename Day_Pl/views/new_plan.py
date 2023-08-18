import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Day_Pl.models import Place, PlaceType, Preference, Plan, PlanPlace
from data_process.constant import area_kor_to_eng
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime, date

@login_required
def index(request):
    placetypes = PlaceType.objects.all()
    current_date = date.today()

    context = {
        'placetypes' : placetypes,
        'current_date' : current_date,
    }

    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('plantitle')
        place_ids = data.get('placeids')
        is_liked = data.get('isliked')

        user = request.user
        created_at = datetime.now()
        # hashtag_area =
        # hashtag_type =
        # hashtag_pick =

        try:
            new_plan = Plan.objects.create(
                created_at = created_at,
                user_id = user,
                title = title,
            )

            if is_liked:
                new_plan.like_users.add(user)
            
            for idx, place_id in enumerate(place_ids):
                if place_id == None:
                    PlanPlace.objects.create(
                        plan = new_plan,
                        order = idx,
                    )
                else:
                    place_obj = Place.objects.get(id = place_id)
                    PlanPlace.objects.create(
                        plan = new_plan,
                        place = place_obj,
                        order = idx,
                    )
            
            response = {
                'status': 'success',
            }
        except:
            response = {
                'status': 'fail',
            }
        return JsonResponse(response)
    return render(request, 'new_plan.html', context=context)

def get_filter(request, placetype_id):
    print(placetype_id)
    if placetype_id:
        places = Place.objects.filter(type_code_id = placetype_id)
    else:
        places = Place.objects.all()[1:]
    # print(places)

    places_json = serializers.serialize('json', places)
    # print(places_json)

    return HttpResponse(places_json, content_type="text/json-comment-filtered")

def check_like(request, place_id):
    place = Place.objects.get(pk=place_id)
    if place.like_users.filter(pk=request.user.pk).exists():
        response = {
            'is_liked': True,
        }
    else:
        response = {
            'is_liked': False,
        }
    return JsonResponse(response)

def get_naver_map(request):
    return render(request, 'components/naver_map_container.html', context=context)