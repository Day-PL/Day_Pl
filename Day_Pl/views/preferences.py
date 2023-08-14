from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Preference, PlaceType

@login_required
def index(request):
    preference_choices = [placetype.code for placetype in PlaceType.objects.all()]
    # print(preference_choices)

    user_preference = Preference.objects.get(user = request.user).prefer.code


    context = {'preference_choices' : preference_choices,
               }
    return render(request, 'preferences.html' , context = context)



# @login_required
# def index(request):
#     #! 기존의 preference 불러오기 (회원가입 완료즉시 False로 만들어줘야함 -> 이후 이 창 뜸)
#     #? 다른 방법은 없을까?
#     user_preference = Preference.objects.get(id = request.user.id)
#     # user_preference = UserPreference.objects.get(user = request.user)
#     # print(2, user_preference)
    
#     #! 유저의 UserPreference 테이블 데이터 가져오기 (True / False)
#     content = {
#         'amusement_park' : user_preference.amusement_park,
#         'zoo' : user_preference.zoo,
#         'plant' : user_preference.plant,
#         'walk' : user_preference.walk,
#         'bike' : user_preference.bike,
#         'skate' : user_preference.skate,
#         'hike' : user_preference.hike,
#         'aquarium' : user_preference.aquarium,
#         'spa' : user_preference.spa,
#         'shopping' : user_preference.shopping,
#         'movie' : user_preference.movie,
#         'cafe' : user_preference.cafe,
#         'cartoon' : user_preference.cartoon,
#         'dog' : user_preference.dog,
#         'cat' : user_preference.cat,
#         'cooking' : user_preference.cooking,
#         'perfume' : user_preference.perfume,
#         'ceramic' : user_preference.ceramic,
#         'ring' : user_preference.ring,
#         'alcohol': user_preference.alcohol,
#         'drawing' : user_preference.drawing,
#         'dance' : user_preference.dance,
#         'flower' : user_preference.flower,
#         'boardgame' : user_preference.boardgame,
#         'escaperoom' : user_preference.escaperoom,
#         'gameroom' : user_preference.gameroom,
#         'screen_baseball' : user_preference.screen_baseball,
#         'bawling' : user_preference.bawling,
#         'musical' : user_preference.musical,
#         'play' : user_preference.play,
#         'concert' : user_preference.concert,
#         'exhibition' : user_preference.exhibition
#     }
#     print(f'before: {content}')

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
