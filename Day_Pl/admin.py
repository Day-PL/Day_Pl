from django.contrib import admin
from .models import *

#? Register your models here.
admin.site.register(UserCourse)
admin.site.register(UserCourseLike)
admin.site.register(Place)
admin.site.register(UserPlaceLike)
admin.site.register(UserPreference)