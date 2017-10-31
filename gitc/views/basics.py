from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from webserver.settings import TOKEN
from webserver.plagin import APITEXT,WEBTEXT
from django.db.models import Sum
from bmpdata.models import *
from bmpdata import initial
from gitc.gform import *
import json

@login_required
def notfind(request):
    return render(request,'404.html')


@login_required
def changepwd(request):
    domain_list = Domain.objects.all()
    if request.method == 'GET':
        obj = ChangepwdForm()
        return render(request, 'changepwd.html', locals())
    else:

        obj = ChangepwdForm(request.POST)
        if obj.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return redirect('/gitcadmin/index.html')
            else:
                oldpassword_is_wrong = True
                errmsg = '原密码不正确！请重新输入！'
                return render(request, 'changepwd.html', locals())
        else:
            oldpassword_is_wrong = True
            errmsg = '2次输入密码不正确！'
            return render(request, 'changepwd.html', locals())


@login_required
def indexview(request):
    page = Page.objects.all().count()
    jiabin = Personnel.objects.all().count()
    yhs = Contact.objects.all().count()
    goupiao = Bill.objects.count()
    shoufei_data = Bill.objects.all().values_list("price")
    shoufei = sum([i[0] for i in shoufei_data]) 
    tp = Imgs.objects.all().count()
    domain_list = Domain.objects.all()
    token = TOKEN
    api = APITEXT
    web = WEBTEXT
    initial.InitialData()
    return render(request, 'index.html', locals())




@login_required
def delcontact(request, cid):
    ret = Contact.objects.filter(id=cid).delete()
    if ret:
        return HttpResponse(json.dumps({'status': True}))
    return HttpResponse(json.dumps({'status': False}))


def loginview(request):
    title = 'GITC后台管理'
    if request.method == 'GET':
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        username = request.POST.get('username')
        pasw = request.POST.get('password')
        user = authenticate(username=username, password=pasw)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/gitcadmin/index.html'))
        error = '账号或密码错误！'
        return render(request, 'login.html', locals())


def logoutview(request):
    logout(request)
    return redirect('/gitcadmin/login.html')


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html',locals())


def permission_denied(request):
    return render(request, '403.html')
