from django.db import models
from django.contrib.auth.models import User
import uuid

class PlaceType(models.Model):
    code = models.CharField(max_length=32, default='Z0', unique=True)
    name = models.CharField(max_length=32, null=False)

class Place(models.Model):
    uuid = models.UUIDField(max_length=128, default=uuid.uuid4)
    name = models.CharField(max_length=64, blank=False)
    type_code = models.ForeignKey(PlaceType, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField(null=True)
    review_total = models.IntegerField(null=True)
    address_si = models.CharField(max_length=32, blank=False)
    address_gu = models.CharField(max_length=32, blank=False)
    address_dong = models.CharField(max_length=32, blank=False)
    address_detail = models.CharField(max_length=32, blank=True)
    contact = models.CharField(max_length=16, blank=False)
    period_start = models.DateTimeField(null=True)
    period_end = models.DateTimeField(null=True)
    expected_time = models.IntegerField()
    url = models.CharField(max_length=128, null=True)
    like_users = models.ManyToManyField(User, related_name='place_like_users')
    created_at = models.DateTimeField(null=True) #! 크롤링한 시간을 넣어줄 것이다

class Plan(models.Model):
    uuid = models.UUIDField(max_length=128, blank=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64, default=f'{created_at}의 플랜')
    except_time1 = models.IntegerField(null=True)
    except_time2 = models.IntegerField(null=True)
    except_time3 = models.IntegerField(null=True)
    hashtag_area = models.CharField(max_length=32, blank=True)
    hashtag_type = models.CharField(max_length=32, blank=True)
    hashtag_pick = models.CharField(max_length=32, blank=True)
    like_users = models.ManyToManyField(User, related_name='plan_like_users')
    memo = models.TextField()
    public = models.BooleanField(null=False, default=False)
    removed = models.BooleanField(null=False,default=False)
    removed_at = models.BooleanField(null=True)

class UserPlanView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    prefer = models.ForeignKey(PlaceType, on_delete=models.CASCADE)

class PlanPlace(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    order = models.IntegerField()

# class UserPlaceLike(models.Model):
#     uuid = models.CharField(max_length=128, blank=False)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     place_id = models.ForeignKey(Place, on_delete=models.CASCADE)


# A1 = models.BooleanField(default=True) #! 식당 : 선호도 조사에서 받지는 않음

# A2 = models.BooleanField(default=True)
# # cafe = models.BooleanField(default=True)

# A3 = models.BooleanField(default=True) 
# # pub = models.BooleanField(default=True)

# B1 = models.BooleanField(default=True)
# # walk  = models.BooleanField(default=True)

# B2 = models.BooleanField(default=True)
# # shopping = models.BooleanField(default=True)

# B3 = models.BooleanField(default=True)
# # movie    = models.BooleanField(default=True)

# B4 = models.BooleanField(default=True) #! 원데이클래스

# C1 = models.BooleanField(default=True)
# # cartoon  = models.BooleanField(default=True)

# C2 = models.BooleanField(default=True)
# # dog = models.BooleanField(default=True)

# C3 = models.BooleanField(default=True)
# # cat = models.BooleanField(default=True)

# C4 = models.BooleanField(default=True)
# # boardgame = models.BooleanField(default=True)

# C5 = models.BooleanField(default=True)
# # escaperoom = models.BooleanField(default=True)

# D1 = models.BooleanField(default=True)
# # screen_baseball = models.BooleanField(default=True)

# D2 = models.BooleanField(default=True)
# # bawling = models.BooleanField(default=True)

# D3 = models.BooleanField(default=True)
# # gameroom = models.BooleanField(default=True)

# E1 = models.BooleanField(default=True) #! 추가한 것
# # hike = models.BooleanField(default=True) #! 추가한 것

# E2 = models.BooleanField(default=True) #! 추가한 것
# # bike = models.BooleanField(default=True) #! 추가한 것

# F1 = models.BooleanField(default=True)
# # musical = models.BooleanField(default=True)

# F2 = models.BooleanField(default=True)
# # play = models.BooleanField(default=True)

# F3 = models.BooleanField(default=True)
# # concert = models.BooleanField(default=True)

# F4 = models.BooleanField(default=True)
# # exhibition = models.BooleanField(default=True)

# G1 = models.BooleanField(default=True)
# # amusement_park = models.BooleanField(default=True)

# G2 = models.BooleanField(default=True)
# # zoo    = models.BooleanField(default=True)

# G3 = models.BooleanField(default=True)
# # plant  = models.BooleanField(default=True)

# G4 = models.BooleanField(default=True)
# # aquarium = models.BooleanField(default=True)

# G5 = models.BooleanField(default=True)
# # skate = models.BooleanField(default=True)

# G6 = models.BooleanField(default=True)
# # spa = models.BooleanField(default=True) 