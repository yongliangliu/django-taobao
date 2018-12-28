# _*_ encoding:utf-8 _*_

from django.conf.urls import url,include
from django.contrib import admin

from django.views.generic import TemplateView

import xadmin
from django.views.static import serve

from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,LogoutView
from users.views import IndexView
from organization.views import OrgView
from mxonline.settings import MEDIA_ROOT,MEDIA_URL #,STATIC_ROOT
from django.conf.urls.static import static





urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(),name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),




    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
   # url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    #课程机构url配置
    url(r'^org/', include('organization.urls',namespace="org")),

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 个人中心url配置
    url(r'^users/', include('users.urls', namespace="users")),

]



#全局404页面
handler404='users.views.page_not_found'
handler500='users.views.page.error'