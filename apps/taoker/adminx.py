# -*- coding: utf-8 -*-
__author__ = 'xinghezhao'
__date__ = '17-1-1 下午11:39'

import xadmin

from .models import OriginData
from operation.models import UserGoodAsk


class OriginDataAdmin(object):
    list_display = ['good_code', 'add_price', 'download', 'add_time']  # 显示字段
    #search_fields = ['good_code', 'add_price', 'download']  # 搜索功能
    #list_filter = ['good_code', 'add_price', 'download', 'add_time']  # 过滤器


class UserGoodAskAdmin(object):
    list_display = ['goodurl', 'goodaddprice', 'goodtitle']


xadmin.site.register(OriginData, OriginDataAdmin)
xadmin.site.register(UserGoodAsk, UserGoodAskAdmin)