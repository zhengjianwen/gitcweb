from django.shortcuts import render, redirect, HttpResponse
from gitc.views.baseview import BaseView
from gitc.views.utils import md5
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from webserver.plagin import LibraryTEXT
from bmpdata.models import *
from bmpdata.logview import write_log
from gitc.gform import *
import json


class Addpage(BaseView):
    '''添加页面'''

    @method_decorator(login_required())
    def get(self, request):
        domain_list = Domain.objects.all()
        if len(domain_list) == 0:
            return redirect('/gitcadmin/domain/index.html')
        return render(request, 'admin/addpage.html', locals())

    @method_decorator(login_required())
    def post(self, request):
        '''
        ajax请求,创建页面
        :param request:
        :return:
        '''
        data = {'status': True, 'url': '', 'msg': None}
        obj = PageForm(request.POST)
        if obj.is_valid():
            p_obj = Page.objects.create(**obj.cleaned_data)
            if p_obj:
                data['url'] = '/gitcadmin/page/%s/index.html' % p_obj.id
                data['msg'] = '创建[ %s ]成功！'% p_obj.name
            else:
                data['status'] = False
                data['msg'] = '没有创建成功！'
        else:
            data['status'] = False
            data['msg'] = '验证未通过！'
        self.write_log(request.user,1,'创建页面，结果为：%s' % data['msg'])
        return HttpResponse(json.dumps(data))


# 管理页
class UPageView(BaseView):

    @method_decorator(login_required())
    def get(self, request, cid):
        domain_list = Domain.objects.all()
        obj = Page.objects.filter(id=cid).first()
        text = []
        library_list = Library.objects.filter(ptl__page=obj).order_by("-weight")
        return render(request, 'admin/pagelist.html', locals())


# 上传图片
@login_required
def upload_kindeditor_img(request):
    '''
    文章的上传图片
    :param request:
    :return:
    '''
    ret = {'error': 0, 'url': '', 'message': '上传成功'}
    if request.method == 'POST':
        page_id = request.GET.get("page",0)
        if page_id:
            doman = Domain.objects.filter(pagetemplate__page__id=page_id).first()
            lib = Library.objects.filter(ptl__page__id=page_id).first()
            file_obj = request.FILES.get('imgFile')
            if not file_obj:
                ret['error'] = 1
                ret['message'] = '没有内容'
            else:
                upfile = BaseView()
                path = upfile.upimg(file_obj,doman,"article",library=lib)
                if path:
                    ret['url'] = path
        else:
            return HttpResponse(json.dumps(ret))
    return HttpResponse(json.dumps(ret))


# 网站管理 查看，编辑，新增
class DomainView(BaseView):
    @method_decorator(login_required())
    def get(self, request):
        domain_list = Domain.objects.all()
        obj = DomainForm()
        return render(request, 'admin/domain.html', locals())

    @method_decorator(login_required())
    def post(self, request):
        domain_list = Domain.objects.all()
        error = ''
        cid = request.POST.get('cid')
        cid = int(cid) if cid else 0

        obj = DomainForm(data=request.POST, status=cid)
        info = {
            'name': request.POST.get('name'),
            'url': request.POST.get('url'),
            'imgpath': request.POST.get('imgpath'),
        }

        if not cid:
            info['token'] = md5()
            ret = Domain.objects.create(**info)
            if not ret: error = '创建网站api失败!'
        else:
            ret = Domain.objects.filter(id=cid).update(**info)
            if not ret: error = '更新网站api失败!'
        return render(request, 'admin/domain.html', locals())


# 插件管理 查看，新增，编辑
class LibraryView(BaseView):
    @method_decorator(login_required())
    def get(self, request):
        text = LibraryTEXT
        domain_list = Domain.objects.all()
        pt_list = PageTemplate.objects.all()
        obj = LibraryForm()
        plagin_count = Plugin.objects.count()
        # 初始化模板
        return render(request, 'admin/library.html', locals())

    @method_decorator(login_required())
    def post(self, request):
        data = {'status': False, 'msg': ''}
        obj = LibraryForm(request.POST)
        try:
            cid = request.POST.get('cid')
            cid = int(cid) if cid else 0
            if obj.is_valid():
                info = {}
                for k, v in obj.cleaned_data.items():
                    if v:
                        info[k] = v
                if cid:
                    ret = Library.objects.filter(id=cid).update(**info)
                else:
                    ret = Library.objects.create(**info)
                data['status'] = True if ret else False
            else:
                data['status'] = False
                data['msg'] = '验证失败'
        except Exception as e:
            data['status'] = False
            data['msg'] = '500'
        return HttpResponse(json.dumps(data))


# 插件删除
class LibraryDel(BaseView):
    def get(self, request, cid):
        data = {'status': True}
        if Library.objects.filter(id=cid).count():
            Library.objects.filter(id=cid).delete()
        else:
            data['status'] = False
        return HttpResponse(json.dumps(data))


# 页面管理
class PageView(BaseView):
    @method_decorator(login_required())
    def get(self, request):
        domain_list = Domain.objects.all()
        page_list = Page.objects.all()
        obj = DomainForm()
        return render(request, 'admin/page.html', locals())

    @method_decorator(login_required())
    def post(self, request):
        data = {'status': False}
        cid = request.POST.get('cid')
        obj = PageForm(request.POST)
        if obj.is_valid():
            ret = Page.objects.filter(id=cid).update(**obj.cleaned_data)
            data['status'] = True if ret else False
        return HttpResponse(json.dumps(data))

# 页面删除
class PageDel(BaseView):
    @method_decorator(login_required())
    def get(self, request, cid):
        data = {'status': True, 'msg': None}
        if Page.objects.filter(id=cid).count():
            img = Imgs.objects.filter(ip__id=cid).count()
            video = Video.objects.filter(vp__id=cid).count()
            article = Article.objects.filter(ap__id=cid).count()
            other = Html.objects.filter(hp__id=cid).count()
            persones = Personnel.objects.filter(ppl__id=cid).count()
            sum_data = img + video + article + other + persones
            if sum_data > 0:
                data['status'] = False
                data['msg'] = '此页面有数据，不能删除此页！'
        else:
            Page.objects.filter(id=cid).delete()
        return HttpResponse(json.dumps(data))


class TemplateView(BaseView):
    @method_decorator(login_required())
    def get(self, request):
        domain_list = Domain.objects.all()
        page_list = Page.objects.all()
        obj = PageTemplateForm()
        return render(request, 'admin/template.html', locals())

    @method_decorator(login_required())
    def post(self, request):
        domain_list = Domain.objects.all()
        page_list = Page.objects.all()
        cid = request.POST.get('cid')
        obj = PageTemplateForm(data=request.POST, files=request.FILES, status=1 if cid else 0)
        domain_id = request.POST.get("domain_id")
        domain = Domain.objects.filter(id=domain_id).first()
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'],domain,'template')
            if cid:
                PageTemplate.objects.filter(id=cid).update(**obj.cleaned_data)
            else:
                PageTemplate.objects.create(**obj.cleaned_data)
        return render(request, 'admin/template.html', locals())


class TemplateDel(BaseView):

    @method_decorator(login_required())
    def get(self, request, cid):
        data = {'status': True}
        if PageTemplate.objects.filter(id=cid).count():
            PageTemplate.objects.filter(id=cid).delete()
        else:
            data['status'] = False
        return HttpResponse(json.dumps(data))


# 邮件类型设置
class MailTypeView(BaseView):

    def get(self,request):
        domain_list = Domain.objects.all()
        mail_group_list = EmailGroup.objects.all()
        obj = EmailGroupForm()
        return render(request,'admin/mailtype.html',locals())

    def post(self,request):
        domain_list = Domain.objects.all()
        cid = request.POST.get('cid')
        try:
            cid = int(cid) if cid else 0
            obj = EmailGroupForm(data=request.POST, status=cid)
            if obj.is_valid():
                if cid:
                    ret = EmailGroup.objects.filter(id=cid).update(**obj.cleaned_data)
                else:
                    ret = EmailGroup.objects.create(**obj.cleaned_data)
        except Exception as e:
            print('MailTypeView---->',e)
        return redirect('/gitcadmin/eamil-type/index.html')


class Mail(BaseView):
    def get(self,request):
        domain_list = Domain.objects.all()
        send_mail_list = Email.objects.filter(eg__effect=1)
        recv_mail_list = EmailGroup.objects.filter(effect=0)
        obj = EmailForm()
        mailtype = EmailGroup.objects.all()
        return render(request, 'admin/email.html', locals())

    def post(self,request):
        cid = request.POST.get('cid')
        try:
            cid = int(cid) if cid else 0
            obj = EmailForm(data=request.POST,status=cid)
            if obj.is_valid():
                if cid:
                    Email.objects.filter(id=cid).update(**obj.cleaned_data)
                else:
                    Email.objects.create(**obj.cleaned_data)
            else:
                error = '验证失败'

        except Exception as e:
            print(e)

        return redirect('/gitcadmin/email/index.html')
