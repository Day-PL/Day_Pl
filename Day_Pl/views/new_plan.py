from django.shortcuts import render, redirect
from Day_Pl.models import Place, PlaceType, Preference
from data_process.constant import area_kor_to_eng
from django.http import HttpResponse
from django.core import serializers
from secret import NAVER_MAP_CLIENT_ID

def index(request):
    places = Place.objects.all()
    placetypes = PlaceType.objects.all()
    print(placetypes)

    context = {
        'places' : places,
        'placetypes' : placetypes,
    }
    return render(request, 'new_plan.html', context=context)

def get_filter(request, placetype_id):
    print(placetype_id)
    if placetype_id:
        places = Place.objects.filter(type_code_id = placetype_id)
    else:
        places = Place.objects.all()
    # print(places)

    places_json = serializers.serialize('json', places)
    # print(places_json)

    return HttpResponse(places_json, content_type="text/json-comment-filtered")

def get_naver_map(request):
    context = {
        'NAVER_MAP_CLIENT_ID': NAVER_MAP_CLIENT_ID,
    }
    return render(request, 'components/naver_map_container.html', context=context)