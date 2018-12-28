# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import  datetime
from django.db import models
from users.models import UserProfile

# Create your models here.



class OriginData(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'原始标题')
    add_price = models.IntegerField(default=0, verbose_name=u'加价')
    url = models.URLField(max_length=200,default='', verbose_name=u"上家地址")
    good_code=models.CharField(max_length=100, verbose_name=u'商家编码')
    download = models.FileField(upload_to='taoke_data/oragin/%Y/%m', verbose_name='原始数据包', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(default="",max_length=20, verbose_name=u'数据包类别')
    tag = models.CharField(default="",max_length=10, verbose_name=u'数据标签')
    image = models.ImageField(default="",upload_to='taoke_data/oragin/%Y/%m', verbose_name=u'商品首图',max_length=100)

    class Meta:
        verbose_name = u'原始数据包'
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.name



class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'服务名称')
    desc = models.CharField(max_length=300, verbose_name=u'服务描述')
    price = models.IntegerField(default=100, verbose_name=u'价格')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'淘客服务商品'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class ServiceBuyLog(models.Model):
    name=models.CharField(default="",max_length=50, verbose_name=u'购买服务名称')
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    service = models.ForeignKey(Service, verbose_name=u'购买的服务')
    mount = models.IntegerField(default=10, verbose_name=u'购买数量')
    rate = models.DecimalField(max_digits=7,decimal_places=2,default=0.97, verbose_name=u'购买折扣')
    total= models.DecimalField(max_digits=7,decimal_places=2,default=0, verbose_name=u'订单总价')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'淘客服务购买记录'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name



class ServiceUseLog(models.Model):
    service = models.ForeignKey(Service, verbose_name=u'购买的服务')
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    class Meta:
        verbose_name = u'淘客服务使用记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name



        # class Service(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name=u'用户')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#
#
# class LieBianChongZhi(models.Model):
#     # 裂变数据包
#     user = models.ForeignKey(UserProfile, verbose_name=u'用户')
#     good_code = models.CharField(max_length=100, verbose_name=u'商家编码')
#     download = models.FileField(upload_to='taoke_data/fenlie', verbose_name='裂变数据包', max_length=100)
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#
#     class Meta:
#         verbose_name = u'列变数据包'
#         verbose_name_plural = verbose_name