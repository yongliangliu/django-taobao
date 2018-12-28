# -*- coding:utf-8 -*-
__date__ = '17/2/24 下午9:08'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile
from operation.models import LieBianData


class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):   #注册
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):   #忘记密码
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):   #重置密码
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['image']



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','address','mobile','qq','alipay_id']



