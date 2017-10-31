from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt
from api.views.base import datavalidate
from api.utils import recvimg,send_self_mail
from api.views.Origin import Response
from bmpdata.models import Meetissue, Contact, Sponsor,Domain,Personnel
from api.apiform import ContactForm, SponsorForm, MeetissueForm
import json,os,time,base64,re


@datavalidate
@csrf_exempt
def ContactApiView(request):
    '''联系我们提交'''
    data = {'status': True, 'msg': None}
    obj = ContactForm(request.POST)
    if obj.is_valid():
        try:
            Contact.objects.create(**obj.cleaned_data)
        except Exception as e:
            data['status'] = False
            data['msg'] = "创建失败"
            return HttpResponse(json.dumps(data, ensure_ascii=False))
        li = []
        dic = {"name": "姓名", "email": "邮件", "phone": "手机", "company": "公司", "department": "部门", "position": "职位",
               "interest": "兴趣", "suggest": "意见", }
        for k, v in obj.cleaned_data.items():
            if k != "code":
                tmp = "%s：%s ;" % (dic[k], v)
                li.append(tmp)
        li.sort()
        maildata = "".join(li)
        ret = send_self_mail("会员咨询邮件",'新会员加入,请尽快联系：%s' % maildata,)
        if ret:
            print("发送成功！")
        else:
            print("发送失败",maildata)
    else:
        data['status'] = False
        data['msg'] = '数据验证失败，'
    return Response(request,data)


def getbase64(req):
    data = req.body.decode("utf-8")
    li = data.split("&")
    for i in li:
        if "photo" in i:
            return i[6:]
    return ""


@datavalidate
@csrf_exempt
def meetissue_add(req):
    '''议题提交'''
    data = {"status": False, "msg": "数据验证失败", "data": None}
    theme = req.POST.get("theme",0)
    phone = req.POST.get("phone",0)
    obj = MeetissueForm(req.POST)
    if Meetissue.objects.filter(theme=theme,phone=phone).count() > 0:
        data["msg"] = "数据已存在，请检查你的主题内容。"
    elif obj.is_valid():
        obj.cleaned_data["ctime"] = str(time.time())
        obj.cleaned_data["photo"] = getbase64(req)
        Meetissue.objects.create(**obj.cleaned_data)
        data["status"] = True
        data["msg"] = "提交成功！"
        hf = '''{company}的 {name}-{position}提交信息。
               信息如下：
                        手   机：{phone}；
                        邮   箱：{email}；
                        地   址：{addr}；
                        个人简介：{summary}；
                        演讲经验：{speech_experience};
                        兴趣专场：{interest};
                        备    注：{remark}
                        演讲主题：{theme}  
                        演讲内容：{content}
                        推 荐 人：{referee}
                        评    分：主题创新 {innovate} 分，
                                  话题热度 {hot_topic} 分，
                                  实战经验 {experience} 分，
                                  通 用 性 {generality} 分；
                        意见建议：{suggest}
                        我的照片： 请前往后台下载！
            '''.format(**obj.cleaned_data)
        send_self_mail("%s的议题提交"%obj.cleaned_data.get("name"),hf)
    return Response(req,data)


@datavalidate
@csrf_exempt
def meetissue_upload(req):
    data = {"status": True, "msg": "", "data": None}
    return Response(req,data)


@datavalidate
@csrf_exempt
def sponsor_add(req):
    '''赞助意向'''
    data = {"status": False, "msg": None, "data": None}
    obj = SponsorForm(req.POST)
    ds_id = req.POST.get("ds_id")
    phone = req.POST.get("phone")
    if Sponsor.objects.filter(phone=phone,ds__id=ds_id).count() > 0:
        data["msg"] = "请勿重复提交，我们稍后会与您联系。"
    elif obj.is_valid():
        obj.cleaned_data["ctime"] = str(time.time())
        Sponsor.objects.create(**obj.cleaned_data)
        data["status"] = True
        data["msg"] = "添加成功，我们会尽快和您联系！"
        hf = """
        姓名：{name},电话：{phone}
        公司名称：{company}
        职位：{position}
        邮箱：{email}
        赞助意向：{intention}
        """.format(**obj.cleaned_data)
        title = "%s想赞助，请尽快与我联系!"%obj.cleaned_data.get("company",obj.cleaned_data.get("name"))
        send_self_mail(title,hf)
    else:
        data["msg"] = "手机号不正确或邮箱格式错误！"
    return Response(req,data)
'''
def makedata(req):
    all_p = Personnel.objects.all()
    for p in all_p:
        pic = str(p.pic)
        pic = pic.replace("wz.92hairui.cn","wz.thegitc.com")
        Personnel.objects.filter(id=p.id).update(pic=pic)
'''
