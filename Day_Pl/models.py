from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Place(models.Model):
    uuid = models.CharField(max_length=128, blank=False)
    name = models.CharField(max_length=64, blank=False)
    type = models.CharField(max_length=64, blank=True) #!
    address_si = models.CharField(max_length=32, blank=False)
    address_gu = models.CharField(max_length=32, blank=False)
    address_dong = models.CharField(max_length=32, blank=False)
    address_detail = models.CharField(max_length=32, blank=True)
    contact = models.CharField(max_length=16, blank=False)
    period_start = models.DateTimeField(null=True) #! 네이밍 다시 생각 (전시회)
    period_end = models.DateTimeField(null=True)   #! 네이밍 다시 생각
    open_time = models.DateTimeField(null=True)
    close_time = models.DateTimeField(null=True)
    expect_time = models.CharField(max_length=32, null=True)
    link = models.CharField(max_length=128, null=True)

class UserCourse(models.Model):
    uuid = models.CharField(max_length=128, blank=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User) #? on_delete=models.CASCADE
    course_name = models.CharField(max_length=64, default = f'{upload_time}의 기록')
    course1_id = models.ForeignKey(Place) #! on_delete=models.CASCADE : 장소 지워지면 코스가 지워져야 하는게 맞는 것 같다 -> on_delete=models.CASCADE이면 이 키만 지워지는 건지 전체가 다 지워지는 건지 확인해야 함
    course2_id = models.ForeignKey(Place)
    course3_id = models.ForeignKey(Place)
    course4_id = models.ForeignKey(Place)
    except_time1 = models.IntegerField(null=True)
    except_time2 = models.IntegerField(null=True)
    except_time3 = models.IntegerField(null=True)
    hashtag_area = models.CharField(max_length=32, blank=True)
    hashtag_type = models.CharField(max_length=32, blank=True)
    hashtag_pick = models.CharField(max_length=32, blank=True)
    like_count = models.ManyToManyField(User, related_name='user_course_like_count') #! 네이밍 다시 생각 (너무 길다)
    memo = models.TextField() #! 네이밍 다시 생각 (너무 길다)

    
class UserCourseLike(models.Model):
    uuid = models.CharField(max_length=128, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(UserCourse, on_delete=models.CASCADE)


class UserPlaceLike(models.Model):
    uuid = models.CharField(max_length=128, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)

class UserPreference(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amusement_park = models.BooleanField(default=True)
    zoo = models.BooleanField(default=True)
    plant = models.BooleanField(default=True)
    walk = models.BooleanField(default=True)
    bike = models.BooleanField(default=True)
    skate = models.BooleanField(default=True)
    hike = models.BooleanField(default=True)
    aquarium = models.BooleanField(default=True)
    spa = models.BooleanField(default=True)
    shopping = models.BooleanField(default=True)
    movie = models.BooleanField(default=True)
    cafe = models.BooleanField(default=True)
    cartoon = models.BooleanField(default=True)
    dog = models.BooleanField(default=True)
    cat = models.BooleanField(default=True)
    cooking = models.BooleanField(default=True)
    perfume = models.BooleanField(default=True)
    ceramic = models.BooleanField(default=True)
    ring = models.BooleanField(default=True)
    alcohol = models.BooleanField(default=True)
    drawing = models.BooleanField(default=True)
    dance = models.BooleanField(default=True)
    flower = models.BooleanField(default=True)
    boardgame = models.BooleanField(default=True)
    escaperoom = models.BooleanField(default=True)
    gameroom = models.BooleanField(default=True)
    screen_baseball = models.BooleanField(default=True)
    bawling = models.BooleanField(default=True)
    musical = models.BooleanField(default=True)
    play = models.BooleanField(default=True)
    concert = models.BooleanField(default=True)
    exhibition = models.BooleanField(default=True)