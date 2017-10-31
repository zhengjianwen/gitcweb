from django.views.decorators.csrf import csrf_exempt
from bmpdata.models import Memberinfo, MemberPCollect, FileCollect, Files, Personnel, Page, Bill
from api.views.Origin import Response
from api.utils import Myredis
from api.utils import Sms, validatecode, validatephone
from api.views.base import datavalidate
import json, time, hashlib, os

myredis = Myredis(redis_db=10)


def get_person_collect(phone, page_id):
    '''处理用户关注人员信息'''
    data = {"date": "", "data": None}
    try:
        p_dic = Page.objects.filter(id=page_id).values()[0]
        data["date"] = p_dic["name"]
        data["id"] = p_dic["id"]
        data["data"] = list(Personnel.objects.filter(memberpcollect__mpc__phone=phone, ppl__id=page_id). \
                            order_by("stime").values("id", "name", "stheme", "sdata", "stime","position","company","pic"))
    except Exception as e:
        print("处理用户关注人员信息:", e)

    return data


def get_file_collect(phone):
    '''处理用户关注w文档信息'''
    data = []
    try:
        data = list(Files.objects.filter(filecollect__mf__phone=phone).order_by("-id").values("id", "name", "url","user__company","user__position"))
    except Exception as e:
        print("处理用户关注文件信息:", e)
    return data


@datavalidate
@csrf_exempt
def userlogin(req, phone):
    '''
    用户登录与注册
    :param req:
    :param phone:
    :return:
    '''
    data = {"status": True, "msg": None, "data": None}
    code = req.POST.get("code", req.POST)
    pphone = req.POST.get("phone", req.POST)
    print(code, req.method)
    if not code:
        data["status"] = False
        data["msg"] = "验证码不能为空！"
    if phone != pphone:
        data["status"] = False
        data["msg"] = "传入值不正确！"
    if not validatecode(phone, code):
        data["status"] = False
        data["msg"] = "验证码不正确！"
    if data["status"]:
        uc = Memberinfo.objects.filter(phone=phone).count()
        if uc == 0:
            u = Memberinfo.objects.create(phone=phone,ctime=str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())))
        else:
            u = Memberinfo.objects.filter(phone=phone).first()
        myredis.login(phone)  # 将状态设置成登录状态
        data["status"] = True
        data["data"] = {"myfiles": get_file_collect(phone),
                        "mycollect": [get_person_collect(phone, 4), get_person_collect(phone, 6)],
                        "name": u.name,
                        "age": u.age,
                        "sex": u.sex,
                        "phone": phone}
        data["msg"] = "登录成功！"
    return Response(req, data,True)


@datavalidate
def add_user_collect(req, phone):
    '''添加用户收藏'''
    data = {"status": False, "msg": "验证失败"}
    pphone = req.POST.get("phone")
    person = req.POST.get("person", 0)
    ret = myredis.islogin(phone)
    if ret and pphone == phone and Personnel.objects.filter(id=person).count() != 0:
        u = Memberinfo.objects.filter(phone=phone).first()
        try:
            MemberPCollect.objects.create(**{"mpc_id": u.id, "mp_id": person})
            data["status"] = True
            data["msg"] = "创建成功"
        except Exception as e:
            data["msg"] = "创建失败"
    return Response(req, data)


@datavalidate
@csrf_exempt
def getmycollect(req, phone):
    '''获取用户收藏信息'''
    data = {"status": True, "msg": None, "data": None}
    myphone = req.POST.get("phone")
    if myphone != phone:
        data["status"] = False
        data["msg"] = "请按照格式请求！"
    uc = Memberinfo.objects.filter(phone=phone).count()
    ret = myredis.islogin(phone)
    if uc != 0 and data["status"] and ret:
        u = Memberinfo.objects.get(phone=phone)
        data["data"] = {"myfiles": get_file_collect(phone),
                        "mycollect": [get_person_collect(phone, 4), get_person_collect(phone, 6)],
                        "name": u.name,
                        "age": u.age,
                        "sex": u.sex,
                        "phone": phone}
    else:
        data["status"] = False
        data["msg"] = "数据验证失败！"
    return Response(req, data)


@datavalidate
@csrf_exempt
def sendsms(req, phone):
    '''发送验证码'''
    data = {"status": False, "msg": "验证失败！"}
    kphone = req.POST.get("phone")
    if kphone == phone:
        s_obj = Sms()
        data = s_obj.sendsms(phone)
    return Response(req, data)


@datavalidate
@csrf_exempt
def add_user_file(req, phone):
    '''创建用户文档收藏信息'''
    data = {"status": False, "msg": "验证失败！"}
    pphone = req.POST.get("phone")
    file_id = req.POST.get("file", 0)
    ret = myredis.islogin(phone)
    if pphone == phone and Files.objects.filter(id=file_id).count() != 0 and ret:
        try:
            u = Memberinfo.objects.filter(phone=phone).first()
            FileCollect.objects.create(**{"mf_id": u.id, "mp_id": file_id})
            data["status"] = True
            data["msg"] = "创建成功"
        except Exception as e:
            print("创建用户文档收藏信息:", e)
            data["msg"] = "创建失败，已收藏!"
    return Response(req, data)


@datavalidate
@csrf_exempt
def user_file_collect(req, phone):
    '''获取用户收藏文档列表'''
    data = {"status": False, "msg": "验证失败！", "data": None}
    pphone = req.POST.get("phone")
    ret = myredis.islogin(phone)
    if pphone != phone:
        data["status"] = False
        data["msg"] = "请按照格式请求！"
    # elif not validatephone(phone):
    #     data["status"] = False
    #     data["msg"] = "手机号验证不正确。"
    if ret and  Memberinfo.objects.filter(phone=phone).count() != 0:
        try:
            data["status"] = True
            data["msg"] = "获取成功"
            data["data"] = get_file_collect(phone)
        except Exception as e:
            print("获取用户收藏文档列表:", e)
            data["msg"] = "500运行错误！"
    return Response(req, data)


@datavalidate
@csrf_exempt
def user_tricket_list(req, phone):
    '''
    获取用户票列表
    :param req:
    :param phone:
    :return:
    '''
    data = {"status": False, "msg": "", "data": None}
    pphone = req.POST.get("phone")
    ret = False
    if pphone == phone:
        data["status"] = True
        ret = myredis.islogin(phone)
    if data["status"] and ret:
        bill_data = Bill.objects.filter(phone=phone).values("id", "code", "sign_staus", "name", "phone","bt__name")
        data["data"] = list(bill_data)
        data["status"] = True
    else:
        data["status"] = False
        data["msg"] = "验证失败，您还没有登录！"
    return Response(req, data)


@datavalidate
@csrf_exempt
def user_tricket(req, phone):
    '''获取单条票务'''
    data = {"status": False, "msg": "", "data": None}
    pphone = req.POST.get("phone")
    cid = req.POST.get("cid")
    ret = False
    if pphone == phone:
        data["status"] = True
        ret = myredis.islogin(phone)
    if ret and data["status"]:
        bill_data = Bill.objects.filter(id=cid, phone=phone).values("code", "sign_staus", "name", "phone","bt__name").first()
        data["data"] = bill_data
        data["status"] = True
        data["msg"] = "获取成功！"
    else:
        data["status"] = False
        data["msg"] = "验证失败，您还没有登录！"
    return Response(req, data)

@datavalidate
@csrf_exempt
def user_logout(req):
    data = {"status": True, "msg": "登出成功", "data": None}
    phone = req.GET.get("phone")
    myredis.delete(phone)
    return Response(req, data)

