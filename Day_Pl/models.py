from django.db import models
from django.contrib.auth.models import User

class PlaceType(models.Model):
    #! id 보안 필요 없을 것 같아 어려운 uuid 삭제
    name = models.CharField(max_length=32, null=False, blank=False)

class Place(models.Model):
    #! id (보안 필요 없을 것 같아 어려운 uuid 삭제)
    uuid           = models.CharField(max_length=128, null=False) 
    name           = models.CharField(max_length=64, blank=False) #! 장소명
    type_id        = models.ForeignKey(PlaceType, default=0)  #! 장소 타입 PlaceType의 id = 0, name = '정보 없음'
    rating         = models.FloatField(null=True, default=0)  #! 평점
    review_total   = models.IntegerField(null=True, default=0) #! 리뷰수
    address_si     = models.CharField(max_length=32, blank=False)
    address_gu     = models.CharField(max_length=32, blank=False)
    address_dong   = models.CharField(max_length=32, blank=False)
    address_detail = models.CharField(max_length=32, blank=True)
    contact        = models.CharField(max_length=16, blank=False)
    period_start   = models.DateTimeField(null=True) #! 네이밍 다시 생각 (전시회)
    period_end     = models.DateTimeField(null=True) #! 네이밍 다시 생각
    open_time      = models.DateTimeField(null=True)
    close_time     = models.DateTimeField(null=True)
    duration       = models.CharField(max_length=32, null=True)
    url            = models.CharField(max_length=128, null=True)
    like_users     = models.ManyToManyField(User, related_name='user_plan_like_count') #? 컬럼명 다시 생각하기
    created_at     = models.DateTimeField(auto_now_add=True)

class Plan(models.Model):
    #! id (보안 필요 없을 것 같아 어려운 uuid 삭제)
    uuid         = models.CharField(max_length=128, null=False) 
    user_id      = models.ForeignKey(User) #? on_delete=models.CASCADE
    created_at   = models.DateTimeField(auto_now_add=True)
    title        = models.CharField(max_length=64, default = f'{created_at}의 플랜')
    modified_at  = models.DateTimeField(null=True) #! 생성시에는 추가 안해줌
    place1_id    = models.ForeignKey(Place, on_delete=models.CASCADE) #! on_delete=models.CASCADE : 지워지면 열 통째로 지우기
    place2_id    = models.ForeignKey(Place, on_delete=models.CASCADE)
    place3_id    = models.ForeignKey(Place, on_delete=models.CASCADE)
    place4_id    = models.ForeignKey(Place, on_delete=models.CASCADE)
    except_time1 = models.IntegerField(null=True)
    except_time2 = models.IntegerField(null=True)
    except_time3 = models.IntegerField(null=True)
    hashtag_area = models.CharField(max_length=32, blank=True)
    hashtag_type = models.CharField(max_length=32, blank=True)
    hashtag_pick = models.CharField(max_length=32, blank=True)
    like_users   = models.ManyToManyField(User, related_name='likers')  #? related_name 다시 생각하기
    view_users   = models.ManyToManyField(User, related_name='viewers') #? related_name 다시 생각하기
    memo         = models.TextField() #! 네이밍 다시 생각 (너무 길다)
    public       = models.BooleanField(null=False, default=False) #! 임시저장을 위한 Column (public = True : 공개)
    removed      = models.BooleanField(null=False, default=False)
    removed_at   = models.DateTimeField(null=True)

class UserPreference(models.Model):
    #! id (보안 필요 없을 것 같아 어려운 uuid 삭제)
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    amusement_park  = models.BooleanField(default=True)
    zoo             = models.BooleanField(default=True)
    plant           = models.BooleanField(default=True)
    walk            = models.BooleanField(default=True)
    bike            = models.BooleanField(default=True)
    skate           = models.BooleanField(default=True)
    hike            = models.BooleanField(default=True)
    aquarium        = models.BooleanField(default=True)
    spa             = models.BooleanField(default=True)
    shopping        = models.BooleanField(default=True)
    movie           = models.BooleanField(default=True)
    cafe            = models.BooleanField(default=True)
    cartoon         = models.BooleanField(default=True)
    dog             = models.BooleanField(default=True)
    cat             = models.BooleanField(default=True)
    cooking         = models.BooleanField(default=True)
    perfume         = models.BooleanField(default=True)
    ceramic         = models.BooleanField(default=True)
    ring            = models.BooleanField(default=True)
    alcohol         = models.BooleanField(default=True)
    drawing         = models.BooleanField(default=True)
    dance           = models.BooleanField(default=True)
    flower          = models.BooleanField(default=True)
    boardgame       = models.BooleanField(default=True)
    escaperoom      = models.BooleanField(default=True)
    gameroom        = models.BooleanField(default=True)
    screen_baseball = models.BooleanField(default=True)
    bawling         = models.BooleanField(default=True)
    musical         = models.BooleanField(default=True)
    play            = models.BooleanField(default=True)
    concert         = models.BooleanField(default=True)
    exhibition      = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(null=True) #! 생성시에는 추가 안해줌

#! 제거!
class UserPlanView(models.Model):
    user_id    = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_id    = models.ForeignKey(Plan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# class UserPlaceLike(models.Model):
#     user_id    = models.ForeignKey(User, on_delete=models.CASCADE)
#     place_id   = models.ForeignKey(Place, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)