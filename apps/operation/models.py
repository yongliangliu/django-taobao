# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name




class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name

class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')),default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读') #布尔类型
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name



class UserGoodAsk(models.Model):
    #提交原始数据包请求
    goodurl = models.URLField(max_length=200,default='', verbose_name=u"上家地址")
    goodaddprice = models.IntegerField(default=50, verbose_name=u'商品加价')
    goodtitle = models.CharField(max_length=50, verbose_name=u'商品标题')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'制数据包请求'
        verbose_name_plural = verbose_name




class UserTitleAsk(models.Model):
    # 提交获取标题请求
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    title_keyword = models.CharField(max_length=200, verbose_name=u'标题关键字')
    titles = models.TextField(default="",max_length=65532, verbose_name=u'标题列表')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'获取标题请求'
        verbose_name_plural = verbose_name


class LieBianData(models.Model):
    # 裂变数据包
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    good_code = models.CharField(max_length=100, verbose_name=u'商家编码')
    download = models.FileField(upload_to='taoke_data/fenlie', verbose_name='裂变数据包', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'列变数据包'
        verbose_name_plural = verbose_name


