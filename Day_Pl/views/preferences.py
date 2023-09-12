from django.shortcuts import render, redirect
from django.urls import reverse
from ..models import Preference, PlaceType, PlaceTypeCategory

def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('common:login'))
    
    preference_choices = PlaceType.objects.all() #! preference_choices의 각 원소는 html 요소의 id값으로 쓰임

    user_preference_ids = [user_preference.prefer.pk for user_preference in  Preference.objects.filter(user = request.user)]

    code_alphabets = PlaceTypeCategory.objects.all()

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
        'code_alphabets' : code_alphabets,
        }
    return render(request, 'preferences.html' , context = context)
