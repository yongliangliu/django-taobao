# -*- coding:utf-8 -*-
__date__ = '17/2/27 下午11:44'

import re
from django import forms
from operation.models import UserGoodAsk,UserTitleAsk


class UserGoodAskForm(forms.ModelForm):
    class Meta:
        model=UserGoodAsk
        fields=['goodurl','goodaddprice','goodtitle']


class UserTitleAskForm(forms.ModelForm):
    class Meta:
        model=UserTitleAsk
        fields=['user','title_keyword']
