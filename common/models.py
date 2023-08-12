import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
<<<<<<< HEAD
    uuid       = models.UUIDField(unique=True, blank=False, default=uuid.uuid4)
=======
    uuid       = models.CharField(max_length=64, blank=False)
    # nickname   = models.CharField(max_length=64, blank=False) #! 추가 예정
>>>>>>> 802d991 (comment : nickname 추가해야 한다)
    fullname   = models.CharField(max_length=64, blank=False)
    # nickname   = models.CharField(max_length=64, blank=True)
    gender     = models.CharField(max_length=64, blank=False)  
    birthdate  = models.DateField(max_length=64, blank=False)
    phone      = models.CharField(max_length=64, blank=False)
    mail       = models.CharField(max_length=64, blank=False)
    rq_terms   = models.BooleanField(default=0)
    op_terms   = models.BooleanField(default=0)
    image      = models.ImageField(upload_to='photos/', null=True, default='static/img/profile_img.png')
    sign_date  = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.user.username