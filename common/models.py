from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    #! ID       : INTEGER AUTO INCREMENT
    #! USERNAME : 아이디
    #! PASSWORD : 비밀번호
    uuid        = models.CharField(max_length=64, blank=False)
    fullname    = models.CharField(max_length=64, blank=False)
    gender      = models.CharField(max_length=64, blank=False)  
    birthdate   = models.DateField(max_length=64, blank=False)
    phone       = models.CharField(max_length=64, blank=False)
    mail        = models.CharField(max_length=64, blank=False)
    rq_terms    = models.BooleanField(default=False)
    op_terms    = models.BooleanField(default=False)
    image       = models.ImageField(upload_to='photos/', null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(null=False, default=True) #! 휴면 계정인지 체크 (회원 탈퇴시 False)
    inactive_at = models.DateTimeField(null=True)              
     #? 두 개를 inactive_at 하나로 관리하는게 좋을까? (장점: 쿼리문을 줄이고, 에러 줄일 수 있다)
     #? 아니면 따로 나누는게 좋을까? (장점: 쿼리문을 이해하기 좋다)