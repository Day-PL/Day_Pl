from django.shortcuts import render, redirect
# from ..models import 

#! <메인 페이지>
#! 인기 TOP3 코스 보여주기
#! 나의 플랜 만들기
def index(request):
    return render(request, 'browse.html')