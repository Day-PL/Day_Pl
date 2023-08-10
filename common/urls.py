from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path("", views.index, name='index'),
    # path('signup/', views.signup, name='signup'), #! 회원가입
    # path('info/', views.info, name='info'), #! 회원정보 수정, 회원 탈퇴
]