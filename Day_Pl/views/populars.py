from django.shortcuts import render, redirect
from ..models import Place, PlaceType, Plan, PlanPlace, Preference

def index(request):
    plans = Plan.objects.all()
    for plan in plans:
        print(plan.title)
        print(plan.like_users.count())
    return render(request, 'populars.html')

def detail(request):
    return render(request, 'populars_detail.html')