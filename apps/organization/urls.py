# -*- coding:utf-8 -*-
__date__ = '17/2/27 下午11:47'


from django.conf.urls import url,include

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView
from .views import OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView

urlpatterns=[
    #课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    #我要学习url
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    #设置课程机构首页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    #设置机构课程页面
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    #设置机构介绍
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    #设置讲师列表
    url(r'^org/teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    #机构收藏请求url
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),


    # 讲师相关url配置
    url(r'^teacher/list$', TeacherListView.as_view(), name="teacher_list"),

    # 设置讲师列表中的详情
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

]