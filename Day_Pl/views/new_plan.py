import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Day_Pl.models import Place, PlaceType, Plan, PlanPlace, PlaceTypeCategory
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.db import transaction
from datetime import datetime, date

@login_required
def index(request):
    places = Place.objects.all()[1:]
    placetype_categories = PlaceTypeCategory.objects.all()
    placetypes = PlaceType.objects.all()
    current_date = date.today()

    context = {
        'places' : places,
        'placetype_categories' : placetype_categories,
        'current_date' : current_date,
    }

    if request.method == 'PUT':
        user = request.user
        data = json.loads(request.body)
        place_id = data.get('placeid')
        place = Place.objects.get(pk=place_id)
        if place.like_users.filter(pk=user.pk).exists():
            place.like_users.remove(user)
            response = {
                'isliked': False,
            }
        else:
            place.like_users.add(user)
            response = {
                'isliked': True,
            }
        return JsonResponse(response)

    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('plantitle')
        place_ids = data.get('placeids')
        is_liked = data.get('isliked')
        hashtag_area = data.get('hashtag_area')
        hashtag_type = data.get('hashtag_type')
        hashtag_pick = data.get('hashtag_pick')
        is_public = data.get('ispublic')

        user = request.user
        created_at = datetime.now()

        with transaction.atomic():
            try:
                new_plan = Plan.objects.create(
                    created_at = created_at,
                    user = user,
                    title = title,
                    hashtag_area = hashtag_area,
                    hashtag_type = hashtag_type,
                    hashtag_pick = hashtag_pick,
                    public = is_public,
                )

                if is_liked:
                    new_plan.like_users.add(user)
                
                for idx, place_id in enumerate(place_ids):
                    if place_id == '':
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
            except Exception:
                # 로그
                transaction.set_rollback(True)
                response = {
                    'status': 'fail',
                }
        return JsonResponse(response)
    return render(request, 'new_plan.html', context=context)

def get_filter(request, placetype_id, search_keyword):
    places = Place.objects.exclude(id=0)
    if placetype_id:
        places = places.filter(type_code__category_id = placetype_id)
    if search_keyword != 'none':
        places = places.filter(Q(name__icontains=search_keyword)|
                                Q(type_code__name__icontains=search_keyword))

    places_json = serializers.serialize('json', places)

    return HttpResponse(places_json, content_type="text/json-comment-filtered")

def get_naver_map(request):
    return render(request, 'components/naver_map_container.html')
