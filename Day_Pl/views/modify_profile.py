from django.shortcuts import render, redirect
from django.urls import reverse
from common.models import Profile
from config.settings import BASE_DIR

def modify_profile(request):
    #! 로그인 안했을 시 로그인창
    if not request.user.is_authenticated:
        return redirect(reverse('common:login'))
    
    #! 회원정보 수정 요청
    if request.method == "POST":
        fullname  = request.POST.get('fullname')
        birthdate = request.POST.get('birthdate')
        phone     = request.POST.get('phone')
        mail      = request.POST.get('mail')
        nickname  = request.POST.get('nickname')
        
        user_profile = Profile.objects.filter(user=request.user)
        user_profile.update(
            fullname  = fullname,
            birthdate = birthdate,
            phone     = phone,
            mail      = mail,
            nickname  = nickname
        )
        return redirect('Day_Pl:modify_profile')

    user_info = {
        'is_authenticated' : request.user.is_authenticated,
        'fullname'         : request.user.profile.fullname,
        'birthdate'        : str(request.user.profile.birthdate).replace('년','-').replace('월','-').replace('일',''),
        'phone'            : request.user.profile.phone,
        'mail'             : request.user.profile.mail,
        'nickname'         : request.user.profile.nickname,
        }
    context = {'user_info' : user_info,
                'user' : request.user,}
    return render(request, 'modify_profile.html', context=context)