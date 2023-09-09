from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Preference, PlaceType

@login_required
def index(request):
    preference_choices = PlaceType.objects.all() #! preference_choices의 각 원소는 html 요소의 id값으로 쓰임

    user_preference_ids = [user_preference.prefer.pk for user_preference in  Preference.objects.filter(user = request.user)]

    if request.method == 'POST':
        for preference_choice in preference_choices:
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
                            'B': '일상 데이트', 'C':'이색카페', 'D':'실내스포츠', 'E':'실외스포츠', 'F':'볼거리', 'G':'특별 데이트'}
        }
    return render(request, 'preferences.html' , context = context)
