from django import forms
from django.core.exceptions import ValidationError
import django.contrib.auth.forms as auth_forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    username = forms.CharField(label='아이디', error_messages={'required': '아이디는 필수 항목입니다.'})
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    fullname = forms.CharField(label='이름', error_messages={'required': '이름은 필수 항목입니다.'})
    nickname = forms.CharField(label='닉네임', error_messages={'required': '닉네임은 필수 항목입니다.'})
    gender = forms.CharField(label='성별', error_messages={'required': '성별은 필수 항목입니다.'})
    birthdate = forms.DateField(label='생년월일', error_messages={'required': '생년월일은 필수 항목입니다.'})
    phone = forms.CharField(label='휴대전화번호', error_messages={'required': '휴대전화번호는 필수 항목입니다.'})
    mail = forms.CharField(label='이메일', error_messages={'required': '이메일은 필수 항목입니다.'})
    class Meta:
        model = Profile
        fields = ('fullname', 'nickname', 'gender', 'birthdate', 'phone', 'mail', 'rq_terms', 'op_terms', 'image')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return phone.replace('-', '')
    
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')
        
        return nickname

    def clean_mail(self):
        mail = self.cleaned_data['mail']
        
        if Profile.objects.filter(mail=mail).exists():
            raise forms.ValidationError('이미 사용 중인 이메일 주소입니다.')
        
        return mail
    
class PasswordResetForm(auth_forms.PasswordResetForm):
    username = auth_forms.UsernameField()

    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise ValidationError('존재하지 않는 사용자입니다.')
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and email:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                profile = Profile.objects.get(user=user)
                if profile.mail != email:
                    raise ValidationError('유효하지 않은 이메일 주소입니다.')
            else:
                raise ValidationError('존재하지 않는 사용자입니다.')



