from django.contrib import admin
from .models import *

admin.site.register(PlaceType)
admin.site.register(Place)
admin.site.register(Plan)
admin.site.register(Preference)