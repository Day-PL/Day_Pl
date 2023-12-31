from django.db import models
from django.contrib.auth.models import User
import uuid

class PlaceTypeCategory(models.Model):
    code = models.CharField(max_length=32, default='Z', unique=True)
    name = models.CharField(max_length=32, null=False)

    def __str__(self) :
        return self.name

class PlaceType(models.Model):
    category = models.ForeignKey(PlaceTypeCategory, on_delete=models.SET_NULL, null=True)
    code           = models.CharField(max_length=32, default='Z0', unique=True)
    name           = models.CharField(max_length=32, null=False)
    
    def __str__(self):
        return self.name

class Place(models.Model):
    uuid                  = models.UUIDField(max_length=128, default=uuid.uuid4)
    name                  = models.CharField(max_length=64, blank=False)
    type_code             = models.ForeignKey(PlaceType, on_delete=models.SET_NULL, null=True)
    type_code_big         = models.CharField(max_length=32, null=True) #! 대분류
    rating                = models.CharField(null=True, max_length=16)
    review_total          = models.IntegerField(null=True, blank=True)
    address_si            = models.CharField(max_length=32, blank=False)
    address_gu            = models.CharField(max_length=32, blank=False)
    address_lo            = models.CharField(max_length=32, blank=False)
    address_detail        = models.CharField(max_length=32, blank=True)
    contact               = models.CharField(max_length=16, blank=True)
    period_start          = models.DateTimeField(null=True, blank=True)
    period_end            = models.DateTimeField(null=True, blank=True)
    expected_time_during  = models.IntegerField(null=True, blank=True)
    url                   = models.CharField(max_length=256, null=True, blank=True) #! 128 넘어서 256으로 업그레이드 함
    like_users            = models.ManyToManyField(User, related_name='place_like_users')
    created_at            = models.DateTimeField(null=True) #! 크롤링한 시간
    lat                   = models.FloatField(null=True)
    lng                   = models.FloatField(null=True)
    naver_place_id        = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    uuid         = models.UUIDField(max_length=128, default=uuid.uuid4)
    created_at   = models.DateTimeField(auto_now_add=True)
    modified_at  = models.DateTimeField(null=True)
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title        = models.CharField(max_length=64, default=f'{created_at}의 플랜')
    hashtag_area = models.CharField(max_length=32, blank=True)
    hashtag_type = models.CharField(max_length=32, blank=True)
    hashtag_pick = models.CharField(max_length=32, blank=True)
    like_users   = models.ManyToManyField(User, related_name='like_plans')
    view_users   = models.ManyToManyField(User, related_name='view_plans', through='UserPlanView')
    memo         = models.TextField(blank=True, null=True)
    public       = models.BooleanField(null=False, default=True)
    removed_at   = models.DateTimeField(blank=True, null=True)
    total_time   = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.title

class UserPlanView(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    plan         = models.ForeignKey(Plan, on_delete=models.CASCADE)
    view_at      = models.DateTimeField(auto_now=True, null=False)

class Preference(models.Model):
    user   = models.ForeignKey(User,      on_delete=models.CASCADE) 
    prefer = models.ForeignKey(PlaceType, on_delete=models.CASCADE)

class PlanPlace(models.Model):
    plan                    = models.ForeignKey(Plan, on_delete=models.CASCADE)
    place                   = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, default=0)
    order                   = models.IntegerField()
    expected_time_from_this = models.IntegerField(blank=True, null=True)
    road_url                = models.CharField(max_length=256, blank=True, null=True)

class PlaceComment(models.Model):
    place       = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comments')
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True) #! 최초 생성시 바뀜
    modified_at = models.DateTimeField(auto_now=True) #! 수정되면 같이 바뀜

class PlanComment(models.Model):
    plan       = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='comments')
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True) #! 최초 생성시 바뀜
    modified_at = models.DateTimeField(auto_now=True) #! 수정되면 같이 바뀜