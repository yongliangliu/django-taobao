# -*- coding:utf-8 -*-
__date__ = '17/2/23 下午11:38'

import xadmin
from xadmin import views
from .models import EmailVerfyRecode,Banner



class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

class GlobalSetting(object):
    site_title="淘客后台管理系统"
    site_footer="淘客在线网"
    menu_style="accordion"


class EmailVerfyRecodeAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display=['title','image','url','index','add_time']
    search_fields=['title','image','url','index']
    list_filter=['title','index','add_time']

xadmin.site.register(EmailVerfyRecode,EmailVerfyRecodeAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)