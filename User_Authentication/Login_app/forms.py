from django import forms
from django.contrib.auth.models import User
from Login_app.models import UserInfo

class UserForm(forms.ModelForm):
    #overwritting password fields
    password = forms.CharField(widget=forms.PasswordInput()) 
    class Meta():
        # taking value from admin User
        model = User
        fields = ('username', 'password', 'email')

class UserInfoForm(forms.ModelForm):
    class Meta():
        model = UserInfo
        fields = ('facebook_id', 'profile_pic')
