from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Domain, Ticket
from bmpdata.logview import write_log
from gitc.gform import TicketForm
import json,time


class TicketView(View):

    @method_decorator(login_required)
    def get(self,req):
        domain_list = Domain.objects.all()
        obj = TicketForm()
        text = ["1.自定义票编码，规则如下",
                "{y} 代表当前年份：2017",
                "{m} 代表当前月份：1-12",
                "{d} 代表当前日：01-31",
                "{random|nub} 代表生成随机数字，nub为整数 1 - 32"
                ]
        return render(req,"admin/ticketlist.html",locals())

    @method_decorator(login_required)
    def post(self,req):
        domain_list = Domain.objects.all()
        obj = TicketForm(req.POST)
        if obj.is_valid():
            try:
                Ticket.objects.create(**obj.cleaned_data)
            except Exception as e:
                print("创建票务错误：",e)
        return render(req,"admin/ticketlist.html",locals())


class TicketEdit(View):

    @method_decorator(login_required)
    def post(self,req):
        data = {"status":True,"msg":None}
        obj = TicketForm(req.POST)
        if obj.is_valid():
            cid = req.POST.get("cid",0)
            try:
                info = {"name":obj.cleaned_data["name"],
                        "weight":obj.cleaned_data["weight"],
                        "code":obj.cleaned_data["code"]}
                Ticket.objects.filter(id=cid).update(**info)
            except Exception as e:
                print("更新票务错误：", e)
                data["msg"] = "更新失败！"
                data["status"] = False
        else:
            data["status"] = False
            data["msg"] = "数据验证失败！"
        return HttpResponse(json.dumps(data,ensure_ascii=False))







