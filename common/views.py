import re
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from common.forms import UserForm, ProfileForm, PasswordResetForm
from datetime import datetime
from .models import Profile

def signup(request):
    current_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(reverse('common:login'))

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

def check_nickname(request):
    data = json.loads(request.body)
    nickname = data.get('nickname')
    
    if Profile.objects.filter(nickname=nickname).exists():
        response = {
            'status': 'fail',
            'message': '이미 사용 중인 닉네입니다.'
        }
    else:
        response = {
            'status': 'success',
            'message': '사용 가능한 닉네임입니다.'
        }
    return JsonResponse(response)

def find_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        if Profile.objects.filter(mail=email).exists():
            user = User.objects.get(profile__mail=email)
            profile = Profile.objects.get(mail=email)
            nickname = profile.nickname
            username = user.username
            send_email(nickname, username, email)
            response = {
                'status': 'success',
            }
        else:
            response = {
                'status': 'error',
                'message': '존재하지 않는 사용자입니다.'
            }
        print(response)
        return JsonResponse(response)
    return render(request, 'auth/find_id.html')

def send_email(nickname, username, mail):
    subject = f"[Day'Pl] {nickname}님의 아이디를 보내드립니다."
    message = render_to_string('find_id_mail.html', {
    'name': nickname,
    'username': username,
	})
    to_email = mail
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset.html'
    success_url = reverse_lazy('common:password_reset_done')
    form_class = PasswordResetForm
    email_template_name = 'auth/password_reset_email.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('common:login')