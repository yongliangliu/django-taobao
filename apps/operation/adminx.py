# -*- coding: utf-8 -*-
__author__ = 'xinghezhao'
__date__ = '17-1-1 下午11:41'

import xadmin

from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
from taoker.models import ServiceUseLog,Service,ServiceBuyLog


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']  # 显示字段
    search_fields = ['name', 'mobile', 'course_name']  # 搜索功能
    list_filter = ['name', 'mobile', 'course_name', 'add_time']  # 过滤器


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']  # 显示字段
    search_fields = ['user', 'course', 'comments']  # 搜索功能
    list_filter = ['user', 'course', 'comments', 'add_time']  # 过滤器


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 显示字段
    search_fields = ['user', 'fav_id', 'fav_type']  # 搜索功能
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 过滤器


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 显示字段
    search_fields = ['user', 'message', 'has_read']  # 搜索功能
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 过滤器


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']  # 显示字段
    search_fields = ['user', 'course']  # 搜索功能
    list_filter = ['user', 'course', 'add_time']  # 过滤器


class ServiceUseLogAdmin(object):
    list_display = ['user', 'service', 'add_time']  # 显示字段
    search_fields =['user', 'service']  # 搜索功能
    list_filter = ['user', 'service', 'add_time']  # 过滤器

class ServiceAdmin(object):
    list_display = ['name', 'price', 'add_time']  # 显示字段
    search_fields = ['name', 'price', 'add_time']  # 搜索功能
    list_filter = ['name', 'price', 'add_time']  # 过滤器

class ServiceBuyLogAdmin(object):
    list_display = ['user', 'service', 'mount','total','rate','add_time']  # 显示字段
    search_fields = ['user', 'service']  # 搜索功能
    list_filter = ['user', 'service', 'add_time']  # 过滤器





xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)


xadmin.site.register(Service, ServiceAdmin)
xadmin.site.register(ServiceBuyLog, ServiceBuyLogAdmin)
xadmin.site.register(ServiceUseLog, ServiceUseLogAdmin)


