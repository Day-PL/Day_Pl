from django.urls import path
from django.urls.base import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path("", views.index, name='index'),
    path('new-user/', views.signup, name='signup'), #! 회원가입
    path('new-user/check-username/', views.check_username, name='check-username'),
    path('new-user/check-mail/', views.check_mail, name='check-mail'),
    path('new-user/check-nickname/', views.check_nickname, name='check-nickname'),
    path('find-id/', views.find_id, name='find-id'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('info/', views.info, name='info'), #! 회원정보 수정, 회원 탈퇴
]