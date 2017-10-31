from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from bmpdata.models import Sponsor, Meetissue, Contact, Domain, Memberinfo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from gitc.pages import Pagination
from gitc.gform import MemberForm
from gitc.views.utils import Export_data
import json


@login_required
def contact(request):
    p = request.GET.get('p', 1)
    url = '/gitcadmin/contact.html'
    pagemax_nub = 10  # 每页显示几条数据
    maxPageNu = 7  # 最大显示几页
    data = Contact.objects.all().order_by('-creat_at')
    page_obj = Pagination(data.count(), p, url, pagemax_nub, maxPageNu)
    data = data[page_obj.start:page_obj.end]
    domain_list = Domain.objects.all()
    return render(request, 'admin/contactlist.html', locals())


@login_required
def sponsorlist(request):
    data = Sponsor.objects.all().order_by("ctime")
    p = request.GET.get('p', 1)
    url = '/gitcadmin/sponsor.html'
    pagemax_nub = 10  # 每页显示几条数据
    maxPageNu = 7  # 最大显示几页
    page_obj = Pagination(data.count(), p, url, pagemax_nub, maxPageNu)
    data = data[page_obj.start:page_obj.end]
    domain_list = Domain.objects.all()
    return render(request, 'admin/sponsor.html', locals())


@login_required
def menmberlist(request):
    '''用户列表'''
    data = Memberinfo.objects.all().order_by("ctime")
    p = request.GET.get('p', 1)
    url = '/gitcadmin/memberlist.html'
    pagemax_nub = 15  # 每页显示几条数据
    maxPageNu = 7  # 最大显示几页
    page_obj = Pagination(data.count(), p, url, pagemax_nub, maxPageNu)
    data = data[page_obj.start:page_obj.end]
    domain_list = Domain.objects.all()
    return render(request, 'admin/member.html', locals())


@login_required
def meetissuelist(request):
    '''议题列表'''
    data = Meetissue.objects.all().order_by("ctime")
    p = request.GET.get('p', 1)
    url = '/gitcadmin/meetissue.html'
    pagemax_nub = 10  # 每页显示几条数据
    maxPageNu = 7  # 最大显示几页
    page_obj = Pagination(data.count(), p, url, pagemax_nub, maxPageNu)
    data = data[page_obj.start:page_obj.end]
    domain_list = Domain.objects.all()
    return render(request, 'admin/meetissue.html', locals())


@login_required
def delmenber(req, cid):
    data = {"status": True, "msg": ""}
    if not Memberinfo.objects.filter(id=cid).delete():
        data["status"] = False
        data["msg"] = "删除失败!"
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
def make_excel_menber(req,bid):
    data = {"status": True, "msg": "生成成功","url":None}
    tmp = {"phone":"手机号","name":"姓名","sex":"性别","age":"年龄",
           "email":"邮箱","company":"公司名称","position":"职位","ctime":"创建时间"}
    keys = req.GET.getlist("keys")
    if not keys:keys = [key for key in tmp]
    keys = sorted(list(set(keys)))
    title = [tmp.get(key,key) for key in keys]
    data_list = Sponsor.objects.filter(ds__id=bid).values()
    obj = Export_data(data_list,keys,title)
    url = obj.down_url()
    data["status"] = True if url else False
    data["msg"] = "生成成功！" if url else "生成失败！"
    data["url"] = url
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
def delsponsor(req, cid):
    data = {"status": True, "msg": ""}
    if not Sponsor.objects.filter(id=cid).delete():
        data["status"] = False
        data["msg"] = "删除失败!"
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
def make_excel_sponsor(req,bid):
    data = {"status": True, "msg": "生成成功","url":None}
    tmp = {"phone":"手机号","name":"姓名","company":"公司名称","position":"职位",
           "email":"邮箱","intention":"票名称","ctime":"提交时间",}
    keys = req.GET.getlist("keys")
    if not keys:
        keys = [key for key in tmp]
    keys = sorted(list(set(keys)))
    title = [tmp.get(key,key) for key in keys]
    data_list = Sponsor.objects.filter(ds__id=bid).values()
    obj = Export_data(data_list,keys,title)
    url = obj.down_url()
    data["status"] = True if url else False
    data["msg"] = "生成成功！" if url else "生成失败！"
    data["url"] = url
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
def delmeetissue(req, cid):
    data = {"status": True, "msg": ""}
    if not Meetissue.objects.filter(id=cid).delete():
        data["status"] = False
        data["msg"] = "删除失败!"
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
def make_excel_meetissue(req,bid):
    data = {"status": True, "msg": "生成成功","url":None}
    tmp = {"phone":"手机号","code":"票号","name":"姓名","order_time":"订单时间","order_nub":"订单号","bt":"票名称","price":"价格",
           "channel":"渠道","channel_code":"渠道编码","sign_staus":"签到状态","sign_time":"签到时间"}
    keys = req.GET.getlist("keys")
    if not keys:
        keys = [key for key in tmp]
    keys = sorted(list(set(keys)))
    title = [tmp.get(key,key) for key in keys]
    bill_list = Meetissue.objects.filter(dm__id=bid).values()
    obj = Export_data(bill_list,keys,title)
    url = obj.down_url()
    data["status"] = True if url else False
    data["msg"] = "生成成功！" if url else "生成失败！"
    data["url"] = url
    return HttpResponse(json.dumps(data, ensure_ascii=False))


class MemberEdita(View):
    @method_decorator(login_required)
    def get(self, req, cid):
        u = Memberinfo.objects.filter(id=cid).values().first()
        obj = MemberForm(initial=u)
        return render(req, "admin/memberedit.html", locals())

    @method_decorator(login_required)
    def post(self, req, cid):
        obj = MemberForm(req.POST)
        if obj.is_valid():
            Memberinfo.objects.filter(id=cid).update(**obj.cleaned_data)
            return redirect("/gitcadmin/memberlist.html")
        else:
            u = Memberinfo.objects.filter(id=cid).values().first()
            return render(req, "admin/memberedit.html", locals())
