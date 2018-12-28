# _*_ coding:utf-8 _*_
from django.shortcuts import render

from operation.models import UserGoodAsk,UserTitleAsk,LieBianData
from django.http import HttpResponse
from django.views.generic import View
from operation.forms import UserGoodAskForm,UserTitleAskForm

from utils.good_title import get_all_title,filter_branch
from utils.email_send import random_str
from mxonline.settings import MEDIA_ROOT
import json,codecs,os
from taoker.models import ServiceUseLog,Service,ServiceBuyLog
from operation.models import UserMessage


import traceback

from utils.email_send import send_wechat
# Create your views here.



class UserGoodAskView(View):
    #用户制作数据包请求
    def post(self,request):
        userask_form=UserGoodAskForm(request.POST)
        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)
            send_wechat('制数据包请求','淘客ID:'+str(request.user.id)+'，标题:'+user_ask.goodtitle)

            return  HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加出错"}', content_type='application/json')



class UserTitleAskView(View):
    #用户标题获取请求
    def post(self,request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg": "用户未登录"}', content_type='application/json')
        if len(request.user.alipay_id)<5:
                return HttpResponse('{"status":"fail", "msg": "请完善个人信息！"}', content_type='application/json')
        title_keyword=request.POST.get("title_keyword","")

        good_type = request.POST.get("good_type", "")

        if title_keyword:


            aa=UserTitleAsk.objects.filter(title_keyword=title_keyword).order_by('-add_time')
            if aa:
                titiles=aa[0].titles
                status=1
            else:
                titiles=get_all_title(title_keyword,pages=15)
                status=0



            filter_branch_result=filter_branch(titiles,good_type)


            if status==0:
                title_ask=UserTitleAsk()
                title_ask.title_keyword=title_keyword
                title_ask.user=request.user
                title_ask.titles =titiles
                title_ask.save()


            return_data={}
            return_data['status']='success'
            return_data['msg']='添加成功'
            return_data['title_all']=titiles
            return_data['branch_all'] = filter_branch_result[0]
            return_data['branch_all_distinct'] = filter_branch_result[1]




            return HttpResponse(json.dumps(return_data), content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加失败"}', content_type='application/json')







class data_csv_upload_View(View):
    #用户标题获取请求
    def post(self,request):
        try:
            if not request.user.is_authenticated():
                # 判断用户登录状态
                return HttpResponse('{"status":"fail", "msg": "用户未登录"}', content_type='application/json')

            


            if int(request.user.get_liebian_now())<1:
                return HttpResponse('{"status":"fail", "msg": "已无使用次数，请充值"}', content_type='application/json')







            myFile = request.FILES.get("file",None)

            title_all = request.POST.get("title_all",None)

            if  myFile and title_all:

                if '\r\n' in title_all:
                    title_all = title_all.split('\r\n')
                else:
                    title_all=title_all.split('\n')
                title_all=list(set(title_all))

                if len(title_all)<500:
                    return HttpResponse('{"status":"fail", "msg": "裂变标题数量过少，请核对！"}', content_type='application/json')


                file_path = MEDIA_ROOT+'/' + myFile.name
                file_path_out = MEDIA_ROOT + '/taoke_data/fenlie/'+random_str()+'_' + myFile.name

                if os.path.exists(MEDIA_ROOT + '/taoke_data/fenlie')==False:
                    os.mkdir(MEDIA_ROOT + '/taoke_data/fenlie')


                if os.path.exists(file_path) == True:
                    os.remove(file_path)
                if os.path.exists(file_path_out) == True:
                    os.remove(file_path_out)

                destination = open(file_path, 'wb+')

                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()


                try:


                    with codecs.open(file_path, 'r', 'utf_16') as csvfile:

                        with codecs.open(file_path_out, 'a', 'utf_16') as out_csv_data_temp:
                            rn = 0
                            good_data = ""
                            for line_one in csvfile:






                                line_one=line_one.strip()






                                rn=rn+1

                                if rn==1:
                                    if line_one != u'version 1.00':
                                        return HttpResponse('{"status":"fail", "msg": "文件格式错误，请重新提交"}',
                                                            content_type='application/json')

                                if rn<4:

                                    out_csv_data_temp.write(line_one)
                                    out_csv_data_temp.write('\r\n')
                                if rn>=4:
                                    good_data=good_data+line_one


                            good_data=good_data.split('\t')
                            good_code=good_data[33]
                            for one_title in title_all:
                                good_data[0]=one_title
                                one_good_data='\t'.join(good_data)
                                out_csv_data_temp.write(one_good_data)
                                out_csv_data_temp.write('\r\n')




                            lie_bian_data = LieBianData()
                            lie_bian_data.good_code = good_code[1:-1]
                            lie_bian_data.user = request.user
                            lie_bian_data.download = file_path_out.replace(MEDIA_ROOT,'')[1:]
                            lie_bian_data.save()

                            ServiceUseLog_one = ServiceUseLog()
                            ServiceUseLog_one.user=request.user
                            ServiceUseLog_one.service=Service.objects.filter(name__contains='裂变').order_by('-add_time')[0]
                            ServiceUseLog_one.save()

                            user_message = UserMessage()
                            user_message.user = request.user.id
                            user_message.message = u"您已使用一次裂变工具，剩余次数："+str(request.user.get_liebian_now())
                            user_message.save()




                    if os.path.exists(file_path) == True:
                        os.remove(file_path)






                    return_data={}
                    return_data['status']="fail"
                    return_data['msg']="提交成功，请在我的数据包中下载"


                    return HttpResponse(json.dumps(return_data), content_type='application/json')
                except:
                    return HttpResponse('{"status":"fail", "msg": "文件格式错误，请重新提交"}',content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg": "请使用获取关键字列表工具生成标题"}', content_type='application/json')
        except Exception,e:
            return HttpResponse('{"status":"fail", "msg": "其他故障，请联系系统管理员"}', content_type='application/json')