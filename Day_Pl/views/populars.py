from django.shortcuts import render, redirect
# from ..models import 

def index(request):
    return render(request, 'populars.html')

def detail(request):
    return render(request, 'populars_detail.html')