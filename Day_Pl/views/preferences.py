from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Preference, PlaceType

@login_required
def index(request):
    print(f"현재 로그인 유저: {request.user}  id(pk): {request.user.id}")

    preference_choices = PlaceType.objects.all() #! preference_choices의 각 원소는 html 요소의 id값으로 쓰임
    # for x in preference_choices:
        # print(f"[디버깅] {x.code} {x.name}")

    user_preference_ids = [user_preference.prefer.pk for user_preference in  Preference.objects.filter(user = request.user)]
    print(f"[디버깅] user_preference_ids: {user_preference_ids}")

    if request.method == 'POST':
        for preference_choice in preference_choices:
            print(f"[디버깅] {preference_choice.code} : {request.POST.get(preference_choice.code, 'off')}")
            if request.POST.get(preference_choice.code, 'off') == 'on' and preference_choice.pk not in user_preference_ids:
                #! db에 추가
                Preference.objects.create(prefer_id = preference_choice.pk, user_id = request.user.id)
            if request.POST.get(preference_choice.code, 'off') == 'off' and preference_choice.pk in user_preference_ids:
                #! db에서 제거
                Preference.objects.get(prefer_id = preference_choice.pk, user_id = request.user.id).delete() 
        return redirect('Day_Pl:preferences')
        
    context = {
        'preference_choices' : preference_choices,
        'user_preference_ids'   : user_preference_ids,
        'code_alphabets' : {'A': '먹거리',
                            'B': '일상 데이트', 'C':'이색카페', 'D':'실내스포츠', 'E':'실외스포츠', 'F':'볼거리', 'G':'특별 데아트'}
        }
    return render(request, 'preferences.html' , context = context)



#
#     #! 데이터 받아서
#     if request.method == 'POST':
#         for key in content.keys():
#             value = request.POST.get(key, 'off')
#             print(key, value)
#             if value == 'on':
#                 setattr(user_preference, key, True)
#                 # user_preference.key = True
#                 content[key] = True
#             else:
#                 setattr(user_preference, key, False)
#                 # user_preference.key = False
#                 content[key] = False
#         user_preference.save()
#         print(f'after: {user_preference.amusement_park}, {user_preference.zoo}, {user_preference.plant}')

#     return render(request, 'preferences.html', context = content)
