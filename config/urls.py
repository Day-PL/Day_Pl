from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include('common.urls')),
    path("", include('Day_Pl.urls')),
    path("data_process/", include('data_process.urls')),
]