from django.http import JsonResponse
from Day_Pl.models import Place, Plan

def check_place_like(request, place_id):
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

def check_plan_like(request, plan_id):
    plan = Plan.objects.get(pk=plan_id)
    if plan.like_users.filter(pk=request.user.pk).exists():
        response = {
            'is_liked': True,
        }
    else:
        response = {
            'is_liked': False,
        }
    return JsonResponse(response)