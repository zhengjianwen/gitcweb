from django.shortcuts import render, redirect,HttpResponse
from gitc.views.baseview import BaseView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Personnel,Domain,Page,Library
from bmpdata.logview import write_log
from gitc.views.utils import md5
from gitc.gform import PersonnelForm
import json

# 人员信息处理函数


# 人员处理
class PersonnelView(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'ppl_id': page_id, 'pl_id': library_id}
        persion_info_dict ={}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加人员'
        else:
            if Personnel.objects.filter(id=cid).count():
                persion_info_dict = Personnel.objects.filter(id=cid).values().first()
            else:
                title = '编辑人员'
        obj = PersonnelForm(initial=persion_info_dict)
        return render(request, 'tmp/personedit.html', locals())

    @method_decorator(login_required())
    def post(self, request, page_id, library_id, cid):
        ppl_id = request.POST.get('ppl_id')
        pl_id = request.POST.get('pl_id')
        self.error = []
        if ppl_id != page_id and pl_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})  # 非法用户
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
            doman = Domain.objects.filter(pagetemplate__page=page_obj).first()
        else:
            self.error.append({'msg': '请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
            doman = Domain.objects.filter(pagetemplate__library__id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})
        if int(cid) == 0:
            operation = request.POST.get('operation', 1)
            obj, status = self.creat(request, operation,doman,library_obj)
        else:
            obj, status = self.edit(request, cid, doman,library_obj)
        if status:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request, 'tmp/personedit.html', locals())

    def creat(self, request, operation,doman,library_obj):
        '''

        :param request:
        :param operation:
        :param doman: 所属域名的对象
        :return:
        '''
        status = True
        obj = PersonnelForm(request.POST, request.FILES, status=operation)
        if obj.is_valid():
            if obj.cleaned_data.get('pic'):
                obj.cleaned_data['pic'] = self.upimg(obj.cleaned_data['pic'], doman, 'persones',library=library_obj)  # 测试环境 1
            a = Personnel.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '验证失败,%s' % obj.errors})
        return obj, status

    def edit(self, request, cid, doman,library_obj):
        obj = PersonnelForm(request.POST, request.FILES)
        if obj.is_valid():
            if obj.cleaned_data.get('pic'):
                obj.cleaned_data['pic'] = self.upimg(obj.cleaned_data['pic'], doman,'persones',library=library_obj)
            ret = Personnel.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else False
        return obj, status

'''
class PersonnelDel(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, cid):
        if Personnel.objects.filter(id=cid, ppl_id=page_id).count():
            Personnel.objects.filter(id=cid, ppl_id=page_id).delete()
        return redirect('/gitcadmin/page/%s/index.html' % page_id)
'''

class PersonnelDel(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, cid):
        data = {"status":False,"msg":""}
        if Personnel.objects.filter(id=cid, ppl_id=page_id).count():
            Personnel.objects.filter(id=cid, ppl_id=page_id).delete()
            data["status"] = True
            data["msg"] = "删除成功！"
        return HttpResponse(json.dumps(data,ensure_ascii=False))



# 批量导入人员
class ImportPerson(BaseView):
    '''导入人员信息处理函数'''

    @method_decorator(login_required())
    def get(self, request, page_id, library_id):
        domain_list = Domain.objects.all()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request, 'admin/importuser.html', locals())

    @method_decorator(login_required())
    def post(self, request, page_id, library_id):
        domain_list = Domain.objects.all()
        data = []
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        file = request.FILES.get('file')
        if file:
            data = self.excel_to_dict(file)
        return render(request, 'admin/importuser.html', locals())


# 单独添加人员 ajax

@login_required
def PersonAddAjax(request):
    '''
    数据批量添加接口
    :param request:
    :return:
    '''
    data = {'status': True, 'msg': None}
    page_id = request.POST.get('ppl_id')
    library_id = request.POST.get('pl_id')
    if Page.objects.filter(id=page_id).count() == Library.objects.filter(id=library_id).count():
        obj = PersonnelForm(request.POST)
        if obj.is_valid():
            try:
                obj.cleaned_data["weight"] = 1
                if Personnel.objects.filter(ppl_id=page_id,pl_id=library_id,name=obj.cleaned_data.get("name")).count() > 0:
                    ret = Personnel.objects.filter(ppl_id=page_id,
                                                   pl_id=library_id,
                                                   name=obj.cleaned_data.get("name"),
                                                   company=obj.cleaned_data.get("company")).update(**obj.cleaned_data)
                else:
                    ret = Personnel.objects.create(**obj.cleaned_data)
                if not ret:
                    data['status'] = False
                    data['msg'] = '创建失败'
            except Exception as e:
                print(e)
                data['status'] = False
                data['msg'] = ' %s ' %obj.errors
        else:
            data['status'] = False
            data['msg'] = '数据验证失败'
    return HttpResponse(json.dumps(data,ensure_ascii=False))


# 人员删除
@login_required
def PersonDelAjax(requset, cid):
    '''
    用户删除人员信息处理
    :param requset:
    :param cid: 数据的id
    :return:
    '''
    data = {'status': True, 'msg': None}
    token = requset.GET.get('token')
    if token == md5(cid):
        ret = Personnel.objects.filter(id=cid).delete()
        if not ret:
            data['status'] = False
            data['msg'] = '数据删除失败'
    else:
        data['status'] = False
        data['msg'] = '请求验证失败！'
    return HttpResponse(json.dumps(data))

