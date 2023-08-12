from django.db import models
from django.contrib.auth.models import User

class PlaceType(models.Model):
    name = models.CharField(max_length=32, null=False)

class Place(models.Model):
    uuid = models.CharField(max_length=128, blank=False)
    name = models.CharField(max_length=64, blank=False)
    type_id = models.ForeignKey(PlaceType, on_delete=models.SET_NULL, null=True)
    rating = models.FloatField(null=True)
    review_total = models.IntegerField(null=True)
    address_si = models.CharField(max_length=32, blank=False)
    address_gu = models.CharField(max_length=32, blank=False)
    address_dong = models.CharField(max_length=32, blank=False)
    address_detail = models.CharField(max_length=32, blank=True)
    contact = models.CharField(max_length=16, blank=False)
    period_start = models.DateTimeField(null=True) #! 네이밍 다시 생각 (전시회)
    period_end = models.DateTimeField(null=True)   #! 네이밍 다시 생각
    mon_open_time = models.DateTimeField(null=True)
    mon_close_time = models.DateTimeField(null=True)
    tue_open_time = models.DateTimeField(null=True)
    tue_close_time = models.DateTimeField(null=True)
    wed_open_time = models.DateTimeField(null=True)
    wed_close_time = models.DateTimeField(null=True)
    thu_open_time = models.DateTimeField(null=True)
    thu_close_time = models.DateTimeField(null=True)
    fri_open_time = models.DateTimeField(null=True)
    fri_close_time = models.DateTimeField(null=True)
    sat_open_time = models.DateTimeField(null=True)
    sat_close_time = models.DateTimeField(null=True)
    sun_open_time = models.DateTimeField(null=True)
    sun_close_time = models.DateTimeField(null=True)
    duration = models.CharField(max_length=32, null=True)
    url = models.CharField(max_length=128, null=True)
    like_users = models.ManyToManyField(User, related_name='place_like_users')
    created_at = models.DateTimeField(auto_now_add=True, null=False)

class Plan(models.Model):
    uuid = models.CharField(max_length=128, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64, default = f'{created_at}의 플랜')
    place1_id = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="place1")
    place2_id = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="place2")
    place3_id = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="place3")
    place4_id = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="place4")
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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

# class UserPlaceLike(models.Model):
#     uuid = models.CharField(max_length=128, blank=False)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     place_id = models.ForeignKey(Place, on_delete=models.CASCADE)

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1) #! 장고 내에서는 id로 인식
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE) #? onetoone으로 해야 될 것 같다.
    amusement_park = models.BooleanField(default=True)
    zoo            = models.BooleanField(default=True)
    plant          = models.BooleanField(default=True)

    walk  = models.BooleanField(default=True)
    bike  = models.BooleanField(default=True)
    skate = models.BooleanField(default=True)
    hike  = models.BooleanField(default=True)

    aquarium = models.BooleanField(default=True)
    spa      = models.BooleanField(default=True)
    shopping = models.BooleanField(default=True)
    movie    = models.BooleanField(default=True)
    cafe     = models.BooleanField(default=True)
    cartoon  = models.BooleanField(default=True)
    dog      = models.BooleanField(default=True)
    cat      = models.BooleanField(default=True)
    cooking  = models.BooleanField(default=True)
    perfume  = models.BooleanField(default=True)
    ceramic  = models.BooleanField(default=True)
    ring     = models.BooleanField(default=True)
    alcohol  = models.BooleanField(default=True)
    drawing  = models.BooleanField(default=True)
    dance    = models.BooleanField(default=True)
    flower   = models.BooleanField(default=True)

    boardgame       = models.BooleanField(default=True)
    escaperoom      = models.BooleanField(default=True)
    gameroom        = models.BooleanField(default=True)
    screen_baseball = models.BooleanField(default=True)
    bawling         = models.BooleanField(default=True)
    
    musical    = models.BooleanField(default=True)
    play       = models.BooleanField(default=True)
    concert    = models.BooleanField(default=True)
    exhibition = models.BooleanField(default=True)