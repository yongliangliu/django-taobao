# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import  datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.

class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50,verbose_name=u"姓名",default="")
    birth_day=models.DateField(verbose_name=u"生日",null=True,blank=True)
    gender=models.CharField(max_length=6,choices=(("male",u"男"),("female","女")),default="female")
    address=models.CharField(max_length=100,default=u"")
    mobile=models.CharField(max_length=11,null=True,blank=True)
    qq = models.CharField(max_length=12, default="",verbose_name=u"qq号")
    image=models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100)

    recommand_id = models.CharField(max_length=4, verbose_name=u"推荐人ID", default="1")
    alipay_id = models.CharField(default="",max_length=30, verbose_name=u"支付宝账号")


    class Meta:
        verbose_name=u"用户信息"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.username


    def get_unread_nums(self):
        #获取用户未读消息
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()



    def get_liebian_use(self):
        from taoker.models import Service,ServiceUseLog
        service= Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
        return ServiceUseLog.objects.filter(service=service,user=self).count()

    def get_liebian_buy(self):
        from taoker.models import Service,ServiceBuyLog
        service= Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
        mount=0
        liebian_buy_all=ServiceBuyLog.objects.filter(service=service,user=self)

        for liebian_buy_one in liebian_buy_all:
            mount=mount+int(liebian_buy_one.mount)

        return mount

    def get_liebian_use_current_month(self):
        from taoker.models import Service, ServiceUseLog
        service = Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
        return ServiceUseLog.objects.filter(service=service, user=self,add_time__month=date.today().month).count()

    def get_liebian_use_last_month(self):
        from taoker.models import Service, ServiceUseLog
        service = Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
        return ServiceUseLog.objects.filter(service=service, user=self,add_time__month=date.today().month).count()

    def get_liebian_use_last_time(self):
        from taoker.models import Service, ServiceUseLog
        service = Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
        last_use=ServiceUseLog.objects.filter(service=service, user=self, ).order_by('-add_time')
        if last_use:
            return last_use[0].add_time

    def get_liebian_now(self):
        from taoker.models import Service, ServiceUseLog,ServiceBuyLog
        service = Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
        use_times= ServiceUseLog.objects.filter(service=service, user=self).count()

        mount = 0
        liebian_buy_all = ServiceBuyLog.objects.filter(service=service, user=self)

        for liebian_buy_one in liebian_buy_all:
            mount = mount + int(liebian_buy_one.mount)

        return mount-use_times



class EmailVerfyRecode(models.Model):
    code=models.CharField(max_length=20,verbose_name=u"验证码")
    email=models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type=models.CharField(verbose_name=u"验证码类型",choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改邮箱")),max_length=20)
    send_time=models.DateField(verbose_name=u"发送时间",default=datetime.now)
    is_used = models.BooleanField(verbose_name=u"是否使用", default=False)

    class Meta:
        verbose_name=u"邮箱验证码"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u"标题")
    image=models.ImageField(upload_to="banner/%Y/%m",verbose_name=u"轮播图",max_length=100)
    url=models.URLField(max_length=200,verbose_name=u"访问地址")
    index=models.IntegerField(default=100,verbose_name=u"顺序")
    add_time=models.DateField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"轮播图"
        verbose_name_plural=verbose_name