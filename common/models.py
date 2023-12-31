import uuid
from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid       = models.UUIDField(unique=True, default=uuid.uuid4)
    nickname   = models.CharField(max_length=64, blank=False)
    fullname   = models.CharField(max_length=64, blank=False)
    gender     = models.CharField(max_length=64, blank=False)  
    birthdate  = models.DateField(max_length=64, blank=False)
    phone      = models.CharField(max_length=64, blank=False)
    rq_terms   = models.BooleanField(default=0)
    op_terms   = models.BooleanField(default=0)
    image      = models.ImageField(upload_to='photos/', null=True, default='static/img/profile_img.png')
    sign_date  = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.user.username
