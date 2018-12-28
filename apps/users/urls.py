# -*- coding:utf-8 -*-
__date__ = '17/2/27 下午11:47'


from django.conf.urls import url,include
from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MymessageView
from .views import OriginDataView,ToolView,LieBianDataView,MyOrderView,MyTeamView,MyBuyView
from taoker.views import UserGoodAskView,UserTitleAskView,data_csv_upload_View


urlpatterns=[
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),


    #用户个人中心头像修改
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

    # 用户个人中心修改邮箱发送验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),


    # 我的收藏机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),

    # 我的收藏讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我的收藏课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息
    url(r'^mymessage/$', MymessageView.as_view(), name='mymessage'),

    #原始数据包列表
    url(r'^origindata/$', OriginDataView.as_view(), name="origindata"),

    # 原始数据包列表
    url(r'^tool/$', ToolView.as_view(), name="tool"),

    # 数据包制作请求列表
    url(r'^goodask/$', UserGoodAskView.as_view(), name="goodask"),

    # 标题获取请求列表
    url(r'^titleask/$', UserTitleAskView.as_view(), name="titleask"),


    # 分裂数据包
    url(r'^data_csv_upload/$', data_csv_upload_View.as_view(), name="data_csv_upload"),

    # 我的分裂数据包
    url(r'^my_data/$', LieBianDataView.as_view(), name="my_data"),

    # 我的服务使用记录
    url(r'^my_order/$', MyOrderView.as_view(), name="my_order"),



    # 我的团队
    url(r'^my_team/$', MyTeamView.as_view(), name="my_team"),

    # 我的购买记录
    url(r'^my_buy/$', MyBuyView.as_view(), name="my_buy"),
]