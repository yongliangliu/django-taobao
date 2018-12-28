# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse


# Create your views here.
from .forms import UserAskForm
from .models import CourseOrg,CityDict,Teacher
from courses.models import Course

from operation.models import UserFavorite

class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self,request):
        all_org=CourseOrg.objects.all()


        # 热门机构排名
        hot_orgs = all_org.order_by("-click_nums")[:3]

        all_city=CityDict.objects.all()

        #设置城市过滤标签
        city_id=request.GET.get('city', "")
        if  city_id:
            all_org=all_org.filter(city=int(city_id))

        # 课程机构搜搜
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_org = all_org.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        #设置类别过滤标签
        category=request.GET.get('ct', "")
        if  category:
            all_org=all_org.filter(category=category)


        #设置排序
        sort=request.GET.get('sort',"")
        if sort:
            if sort=="students":
                all_org=all_org.order_by("-students")
            elif sort=="courses":
                all_org = all_org.order_by("-course_nums")



        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org,3,request=request)
        orgs = p.page(page)







        org_nums = all_org.count()




        return render(request,"org-list.html",{
            "all_org":orgs,
            "all_city": all_city,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,

        })


class AddUserAskView(View):
    #用户添加咨询
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)
            return  HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加出错"}', content_type='application/json')



class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request , org_id):
        current_page="home"

        course_org=CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True

        all_courses=course_org.course_set.all()[:3]
        all_teachers=course_org.teacher_set.all()[:1]

        return render(request,'org-detail-homepage.html',{
                'all_courses':all_courses,
                'all_teachers': all_teachers,
                'course_org':course_org,
                'current_page':current_page,
                'has_fav':has_fav,
            })

class OrgCourseView(View):
    #机构课程列表
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
                    'all_courses': all_courses,
                    'course_org': course_org,
                    'current_page':current_page,
                    'has_fav': has_fav,
            })

class OrgDescView(View):
    #机构描述列表
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-desc.html', {
                    'all_courses': all_courses,
                    'course_org': course_org,
                    'current_page':current_page,
                    'has_fav':has_fav,
            })



class OrgTeacherView(View):
    #机构讲师列表
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
                    'all_teachers': all_teachers,
                    'course_org': course_org,
                    'current_page':current_page,
                    'has_fav': has_fav,
            })



class AddFavView(View):
    """
    用户收藏,以及用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)


        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #记录已经存在， 则表示用户取消收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()

            if int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()

            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()


            return HttpResponse('{"status":"success", "msg": "收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                if int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg": "收藏出错"}', content_type='application/json')




class TeacherListView(View):
    #讲师列表页
    def get(self,request):
        all_teachers=Teacher.objects.all()
        #全局搜搜讲师
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))

        #设置排序
        sort=request.GET.get('sort',"")
        if sort:
            if sort=="hot":
                all_teachers=all_teachers.order_by("-click_nums")


        sorted_teacher=Teacher.objects.all().order_by("-click_nums")[:3]


        #对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        all_teachers_count=all_teachers.count()

        p = Paginator(all_teachers,3,request=request)
        teachers = p.page(page)




        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
            'all_teachers_count':all_teachers_count

        })



class TeacherDetailView(View):


    def get(self, request,teacher_id):

        teacher=Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums+=1
        teacher.save()


        hav_teacher_faved=False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            hav_teacher_faved=True

        hav_org_faved=False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
            hav_org_faved=True


        all_courses=Course.objects.filter(teacher=teacher)
        #讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]






        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher,
            'hav_teacher_faved':hav_teacher_faved,
            'hav_org_faved':hav_org_faved,



        })