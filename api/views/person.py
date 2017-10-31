from django.views import View
from django.shortcuts import HttpResponse,redirect,render
from django.views.decorators.csrf import csrf_exempt
from api.views.base import datavalidate
from api.views.Origin import Response
from bmpdata.models import Personnel,Page,Library,PageTemplate,Domain,MemberPCollect,FileCollect
import json, time, hashlib, os


class PersonApiView(View):
    def get(self, request,doman_id,page_id, library_id):
        data = {'status': True, 'data': None}
        try:
            token = request.GET.get('token')
            doman = Domain.objects.filter(id=doman_id, token=token).first()
            if doman:
                title = request.GET.getlist('title', [])
                if not title:
                    dic = list(Personnel.objects.filter(ppl_id=page_id, pl_id=library_id).values('name', 'ename','company','position','pic','summary'))
                else:
                    dic = list(Personnel.objects.filter(ap_id=page_id, al_id=library_id).values(*title))
                if not dic:
                    data['msg'] = 'No data！'
                else:
                    data['data'] = dic
                    data['parameter'] = list(Library.objects.filter(id=library_id).values('width', 'height'))[0]
            else:
                data['status'] = False
                data['msg'] = 'Validation failure'
        except Exception as e:
            data['status'] = False
            data['msg'] = 'God must be joking'
        return Response(request,data)


@datavalidate
@csrf_exempt
def person(req,pid):
    '''获取个人信息'''
    data = {"status": False, "msg": None, "data": None}
    if Personnel.objects.filter(id=pid).count() != 0:
        p_list = Personnel.objects.filter(id=pid).values().first()
        data['data'] = p_list
        data['status'] = True
    else:
        data["msg"] = "传入值不正确！"
    return Response(req,data)


@datavalidate
@csrf_exempt
def personlist(req,library_id):
    data = {"status": False, "msg": None, "data": None}
    phone = req.GET.get("phone", False)
    order_by = req.GET.get("order_by","ename")
    if Library.objects.filter(id=library_id).count() != 0 and phone:
        dic = ["id","pic","meet","summary","stheme","name","meetaddr","company","sintroduce","stime","position","sdata","files__id","files__url"]
        user_c = MemberPCollect.objects.filter(mpc__phone=phone).values("mp__id")
        user_f = FileCollect.objects.filter(mf__phone=phone).values("mp__id")
        user_list = [x["mp__id"] for x in user_c]
        file_list = [x["mp__id"] for x in user_f]
        a_list = list(Personnel.objects.filter(pl__id=library_id).order_by(order_by).values(*dic))
        for pdic in a_list:
            pdic["collect"] = True if pdic["id"] in user_list else False
            pdic["file_collect"] = True if pdic["id"] in file_list else False
        data['data'] = a_list
        data['status'] = True
    else:
        data["msg"] = "传入值不正确！"
    return Response(req,data)


@datavalidate
@csrf_exempt
def page_person(req,page_id):
    data = {"status": False, "msg": None, "data": None}
    page_obj = Page.objects.filter(id=page_id)
    phone = req.GET.get("phone",False)
    datatype = req.GET.get("type",1)
    if page_obj and phone:
        dic = ["id", "pic", "meet", "summary", "stheme", "name", "meetaddr", "company", "sintroduce", "stime","position", "sdata", "files__id", "files__url","meetaddr"]
        user_c = MemberPCollect.objects.filter(mpc__phone=phone).values("mp__id")
        user_list = [x["mp__id"] for x in user_c]
        user_f = FileCollect.objects.filter(mf__phone=phone).values("mp__id")
        file_list = [x["mp__id"] for x in user_f]
        if datatype:
            p_data = []
            lib_list = Library.objects.filter(ptl__page__id=page_id).order_by("-weight")
            for lib in lib_list:
                p_list = list(Personnel.objects.filter(pl=lib).order_by("-weight").values(*dic))
                for pdic in p_list:
                    pdic["collect"] = True if pdic["id"] in user_list else False
                    pdic["file_collect"] = True if pdic["id"] in file_list else False
                tmp = {"name":lib.name,"weight":lib.weight,"data":p_list,"other":lib.other}
                p_data.append(tmp)
            data['data'] = p_data
            data["status"] = True
        else:
            p_data = list(Personnel.objects.filter(ppl__id=page_id).order_by("ename").values(*dic))
            for pdic in p_data:
                pdic["collect"] = True if pdic["id"] in user_list else False
                pdic["file_collect"] = True if pdic["id"] in file_list else False
            data['data'] = p_data
            data["status"] = True
    else:
        data["msg"] = "页面不存在！"
    return Response(req,data)
