from django.shortcuts import render, redirect
from gitc.views.baseview import BaseView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Domain, Page, Library, Html
from bmpdata.logview import write_log
from gitc.gform import HtmlForm
import time



# 自定义模块 增改查
class HtmlView(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'hp_id': page_id, 'hl_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加HTML代码'
        else:
            if Html.objects.filter(id=cid).count():
                html_obj = Html.objects.filter(id=cid).first()
                title = '修改[ %s ]代码' % html_obj.name
                info['name'] = html_obj.name
                info['html'] = html_obj.html
            else:
                title = '添加HTML代码'
        obj = HtmlForm(initial=info)
        return render(request, 'tmp/htmledit.html', locals())

    @method_decorator(login_required())
    def post(self, request, page_id, library_id, cid):
        hp_id = request.POST.get('hp_id')
        hl_id = request.POST.get('hl_id')
        self.error = []
        if hp_id != page_id and hl_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})  # 非法用户
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            self.error.append({'msg': '请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})
        if int(cid) == 0:
            obj, status = self.creat(request)
        else:
            html_obj = Html.objects.filter(id=cid).first()
            obj, status = self.edit(request, cid)
        if status:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request, 'tmp/htmledit.html', locals())

    def creat(self, request):
        status = True
        obj = HtmlForm(request.POST, status=1)
        if obj.is_valid():
            obj.cleaned_data['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            a = Html.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '数据验证失败！'})
        return obj, status

    def edit(self, request, cid):
        obj = HtmlForm(request.POST)
        if obj.is_valid():
            ret = Html.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else False
        return obj, status


# 自定义删除
class HtmlDel(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, cid):
        if Html.objects.filter(id=cid, hp_id=page_id).count():
            Html.objects.filter(id=cid, hp_id=page_id).delete()
        return redirect('/gitcadmin/page/%s/index.html' % page_id)
