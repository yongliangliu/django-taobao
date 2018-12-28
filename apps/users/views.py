# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerfyRecode
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email

from django.http import HttpResponse,HttpResponseRedirect
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #用于分页


from operation.models import UserCourse,UserFavorite,UserMessage,LieBianData
from organization.models import CourseOrg,Teacher
from courses.models import Course
from taoker.models import OriginData,Service,ServiceUseLog,ServiceBuyLog

from .models import Banner
from django.http import HttpResponseRedirect


from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        record = EmailVerfyRecode.objects.filter(code=active_code)
        if record:
            record = record[0]
            if record.is_used==False:




                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()


                user_message = UserMessage()
                user_message.user = user.id
                user_message.message = u"您的账号已激活成功！现赠送5次裂变工具，如有疑问请联系您的推荐人"
                user_message.save()

                server_send=ServiceBuyLog()
                server_send.user=user
                server_send.mount=5
                server_send.rate=0
                server_send.total=int(server_send.mount*server_send.rate)
                server_send.service=Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
                server_send.name=u"激活赠送裂变工具5次"
                server_send.save()

                record.is_used = True
                record.save()





            else:
                return render(request, 'active_done.html')
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerfyRecode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html',{"email":email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class ModifyPwdView(View):
    #修改用户密码
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password1","")
            pwd2=request.POST.get("password2","")
            email=request.POST.get("email","")
            if pwd1 !=pwd2:
                return render(request, 'password_reset.html', {"email": email,"msg":u"密码不一致"})
            else:

                user=UserProfile.objects.get(email=email)
                user.password=make_password(pwd2)
                user.save()
                return render(request, 'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": u"密码不一致"})




class RegisterView(View):  #注册
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user_name=request.POST.get("email","")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form":register_form,"msg": u"用户已存在！"})
            recommand_id = request.POST.get("recommand_id", "")

            if len(recommand_id)==0:
                return render(request, "register.html", {"register_form": register_form, "msg": u"推荐人不存在，请联系你的介绍人"})

            aa=UserProfile.objects.filter(Q(id=int(recommand_id)) & Q(is_active=True))
            if len(aa)==0:
                return render(request, "register.html", {"register_form": register_form, "msg": u"推荐人不存在，请联系你的介绍人"})

            pass_word=request.POST.get("password","")

            user_profile = UserProfile()
            user_profile.username =user_name
            user_profile.email =user_name
            user_profile.recommand_id = recommand_id
            user_profile.is_active=False
            user_profile.password = make_password(pass_word)
            user_profile.save()


            send_email = send_register_email(user_name, "register")


            #写入欢迎注册消息
            user_message=UserMessage()
            user_message.user=user_profile.id
            user_message.message=u"欢迎注册淘客在线网"
            user_message.save()

            user_message = UserMessage()
            user_message.user = user_profile.recommand_id
            user_message.message = u"您的团队有新成员加入，用户名为："+user_name+'，激活码为：http://taoker.online/active/'+send_email['code']
            user_message.save()


            send_register_email(user_name,"register")


            return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_form})
            pass




class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form=LoginForm(request.POST)

        if login_form.is_valid():


            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse  #
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, "index.html", {})
                else:
                    return render(request, "login.html", {"msg": u"用户未激活！"})

            else:
                return render(request, "login.html", {"msg": u"用户名或密码错误！"})

        else:
            return render(request, "login.html", {"login_form":login_form})



#通过类实现退出
class LogoutView(View):
    """
    用户登录
    """
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse #
        return HttpResponseRedirect(reverse('index'))




class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')

            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                return render(request, "forgetpwd.html", {"forget_form": forget_form, "msg": u"该用户不存在！请重新输入正确用户名"})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})




class UserInfoView(LoginRequiredMixin,View):
    #用户个人信息
    def get(self, request):
        return render(request, 'usercenter-info.html',{

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success", "msg": "修改成功"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')




class UploadImageView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        image_form=UploadImageForm(request.POST,request.FILES,instance=request.user)

        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success", "msg": "修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "修改出错"}', content_type='application/json')




class UpdatePwdView(View):
    #个人中心修改用户密码
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password1","")
            pwd2=request.POST.get("password2","")
            if pwd1 !=pwd2:
                return HttpResponse('{"status":"fail", "msg": "密码不一致"}', content_type='application/json')


            user=request.user
            user.password=make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success", "msg": "修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"sucess"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerfyRecode.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"sucess"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')




class MyCourseView(LoginRequiredMixin,View):
    #用户课程信息
    def get(self, request):
        user_courses=UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html',{
            'user_courses':user_courses

        })






class MyFavOrgView(LoginRequiredMixin,View):
    #用户课程信息
    def get(self, request):
        org_list=[]
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id=fav_org.fav_id
            org=CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html',{
            'org_list':org_list

        })


class MyFavTeacherView(LoginRequiredMixin,View):
    #用户收藏用户讲师
    def get(self, request):
        teacher_list=[]
        fav_teachers=UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id=fav_teacher.fav_id
            teacher=CourseOrg.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list

        })




class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """

    def get(self, request):
        course_list = []

        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            teacher = Course.objects.get(id=course_id)
            course_list.append(teacher)

        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list
        })


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        #用户进入个人消息后清空未读消息的记录
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()


        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 15, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages':messages
        })



class IndexView(View):
    def get(self,request):
        #取出轮播图



        all_banners=Banner.objects.all().order_by('index')
        courses=Course.objects.filter(is_banner=False)[:6]

        banner_courses=Course.objects.filter(is_banner=True)[:3]


        return render(request,'index.html',{
            'all_banners':all_banners,
            'banner_courses':banner_courses,
            'courses':courses,

        })


def page_not_found(request):
    #全局404
    from django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


def page_error(request):
    #全局404
    from django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code=500
    return response



class OriginDataView(LoginRequiredMixin,View):
    #最新原始数据包
    def get(self, request):
        origindata_all=OriginData.objects.all().order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(origindata_all, 16, request=request)
        data = p.page(page)

        return render(request, 'usercenter-orgindata.html',{
            'origindata_all':data

        })


class ToolView(LoginRequiredMixin,View):
    #最新原始数据包
    def get(self, request):

        all_buy_log = ServiceBuyLog.objects.filter(user=request.user.id,service=Service.objects.filter(name__contains='裂变').order_by('-add_time')[0])
        liebian_mount_buy_all=0
        for n in all_buy_log:
            liebian_mount_buy_all=liebian_mount_buy_all+n.mount

        liebian_mount_use_all=ServiceUseLog.objects.filter(user=request.user.id,service=Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]).count()


        liebian_mount_now=liebian_mount_buy_all-liebian_mount_use_all











        return render(request, 'usercenter-tool.html',{
            'liebian_mount_all':liebian_mount_now,

        })



class LieBianDataView(LoginRequiredMixin,View):
    #我的数据包
    def get(self, request):
        LieBianData_all=LieBianData.objects.filter(user=request.user.id).order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(LieBianData_all, 10, request=request)
        data = p.page(page)
        return render(request, 'usercenter-mydata.html',{
            'LieBianData_all':data

        })


class MyOrderView(LoginRequiredMixin,View):
    #我的数据包
    def get(self, request):
        ServiceUseLog_all=ServiceUseLog.objects.filter(user=request.user.id).order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(ServiceUseLog_all, 10, request=request)
        data = p.page(page)
        return render(request, 'usercenter-myorder.html',{
            'ServiceUseLog_all':data

        })


class MyTeamView(LoginRequiredMixin,View):
    #我的数据包
    def get(self, request):
        Team_firs_all=UserProfile.objects.filter(recommand_id=request.user.id)


        ids=[]

        for Team_firs_one in Team_firs_all:
            ids.append(Team_firs_one.id)

        #获取我的推荐人
        myrecommand=UserProfile.objects.filter(id=request.user.recommand_id)[0]

        Team_sec_all = UserProfile.objects.filter(recommand_id__in=ids)

        for Team_sec_one in Team_sec_all:
            ids.append(Team_sec_one.id)

        Team_third_all = UserProfile.objects.filter(recommand_id__in=ids)

        for Team_third_one in Team_third_all:
            ids.append(Team_third_one.id)

        ids=list(set(ids))
        

        Team_all=UserProfile.objects.filter(id__in=ids).order_by('-date_joined')

        team_nums=Team_all.count()




        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(Team_all, 20, request=request)
        data = p.page(page)
        return render(request, 'usercenter-myteam.html',{
            'Team_all':data,
            'team_nums':team_nums,
            'myrecommand':myrecommand,

        })


class MyBuyView(LoginRequiredMixin,View):
    #我的数据包
    def get(self, request):
        ServiceBuyLog_all=ServiceBuyLog.objects.filter(user=request.user.id).order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(ServiceBuyLog_all, 10, request=request)
        data = p.page(page)
        return render(request, 'usercenter-mybuy.html',{
            'ServiceBuyLog_all':data

        })
