# -*- coding:utf-8 -*-
__date__ = '17/2/27 下午11:47'


from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddComentsView,VideoPlayView


urlpatterns=[
    #课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),

    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$',  CourseDetailView.as_view(), name="course_detail"),

    # 课程详情页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name="course_comment"),

    #添加课程评论
    url(r'^add_comment/$', AddComentsView.as_view(), name="add_comment"),

    # 课程详情页
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),






    # #课程机构列表页
    # url(r'^list/$', OrgView.as_view(), name="org_list"),
    # #我要学习url
    # url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    # #设置课程机构首页
    # url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    # #设置机构课程页面
    # url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    # #设置机构介绍
    # url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    # #设置讲师列表
    # url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    # #机构收藏请求url
    # url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]