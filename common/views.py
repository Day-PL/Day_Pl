import re
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from common.forms import UserForm, ProfileForm
from datetime import datetime
from Day_Pl.models import Preference # TODO: 이름 바꾸어야 함
from .models import Profile

def signup(request):
    current_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            print('user 저장됨')
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            print('profile 저장됨')

            # Preference 초기화
            Preference.objects.create(user_id=user)
            return redirect('Day_Pl:browse')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'auth/signup.html',\
                  {'user_form': user_form,
                  'profile_form': profile_form,
                  'current_date': current_date})

def check_username(request):
    data = json.loads(request.body)
    username = data.get('username')
    reg = r'^[A-Za-z0-9_-]{4,20}$'

    if User.objects.filter(username=username).exists():
        response = {
            'status': 'fail',
            'message': '이미 사용 중인 아이디입니다.'
        }
    else:
        if not re.search(reg, username):
            response = {
                'status': 'error',
                'message': '4~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.'
            }
        else:
            response = {
                'status': 'success',
                'message': '사용 가능한 아이디입니다.'
            }
    return JsonResponse(response)

def check_mail(request):
    data = json.loads(request.body)
    mail = data.get('mail')
    reg = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if Profile.objects.filter(mail=mail).exists():
        response = {
            'status': 'fail',
            'message': '이미 사용 중인 이메일입니다.'
        }
    else:
        if not re.search(reg, mail):
            response = {
                'status': 'error',
                'message': '이메일 주소가 정확한지 확인해 주세요.'
            }
        else:
            response = {
                'status': 'success',
                'message': '사용 가능한 이메일입니다.'
            }
    return JsonResponse(response)