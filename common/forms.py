from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fullname', 'gender', 'birthdate', 'phone', 'mail', 'rq_terms', 'op_terms', 'image')
        # TODO: 닉네임 추후 추가

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return phone.replace('-', '')
    
    # def clean_nickname(self):
    #     nickname = self.cleaned_data['nickname']
    #     if nickname == '':
    #         nickname = # 랜덤데이터 생성
    #         return nickname
    #     return nickname