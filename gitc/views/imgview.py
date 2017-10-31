from django.shortcuts import render, redirect,HttpResponse
from gitc.views.baseview import BaseView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Imgs,Domain,Library,Page
from bmpdata.logview import write_log
from gitc.gform import ImgsForm
import time,json


# 图片处理
class ImgView(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'ip_id': page_id, 'il_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加图片'
        else:
            if Imgs.objects.filter(id=cid).count():
                img_obj = Imgs.objects.filter(id=cid).first()
                title = '修改[ %s ]图片' % img_obj.title
                info['title'] = img_obj.title
                info['content'] = img_obj.content
                info['url'] = img_obj.url
                info['img'] = img_obj.img
            else:
                title = '添加图片'
        obj = ImgsForm(initial=info)
        return render(request, 'tmp/imgedit.html', locals())

    @method_decorator(login_required())
    def post(self, request, page_id, library_id, cid):
        ip_id = request.POST.get('ip_id')
        il_id = request.POST.get('il_id')
        self.error = []
        if ip_id != page_id and il_id != library_id:
            self.error.append({'msg': '请勿私自修改代码参数，验证不通过！；'})  # 非法用户
            doman = Domain.objects.filter(pagetemplate__library__id=library_id).first()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
            doman = Domain.objects.filter(pagetemplate__page=page_obj).first()
        else:
            self.error.append({'msg': '请求页面不存在或已被删除；'})
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            self.error.append({'msg': '请求地址不正确，请勿私自填写地址！'})

        if int(cid) == 0:
            obj, status = self.creat(request,doman,library_obj)
        else:
            obj, status = self.edit(request, cid,doman,library_obj)
        if status:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request, 'tmp/imgedit.html', locals())

    def creat(self, request,doman,library_obj):
        status = True
        obj = ImgsForm(request.POST, request.FILES, status=1)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'],doman, 'images',library=library_obj)
            else:
                del obj.cleaned_data['img']
            obj.cleaned_data['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            a = Imgs.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                msg = '数据创建失败'
                self.error.append({'msg':msg })
            else:
                msg = '创建成功'
        else:
            status = False
            msg = '图片不能为空，请重新上传！'
            self.error.append({'msg': msg})
        write_log(request.user, 1, '创建图片信息，结果为：%s' % msg)
        return obj, status

    def edit(self, request, cid,domain,library_obj):
        obj = ImgsForm(request.POST, request.FILES)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'],domain, 'images',library=library_obj)
            else:
                del obj.cleaned_data['img']
            old_list = list(Imgs.objects.filter(id=cid).values())[0]
            ret = Imgs.objects.filter(id=cid).update(**obj.cleaned_data)
            new_list = list(Imgs.objects.filter(id=cid).values())[0]
            print(old_list,new_list)
            status = True if ret else  False
        return obj, status


# 图片删除
class ImgDel(BaseView):
    @method_decorator(login_required())
    def get(self,request,page_id,cid):
        data = {"status":False,"msg":"传入值错误"}
        nub = Imgs.objects.filter(id=cid,ip_id=page_id).count()
        print(nub)
        if nub > 0:
            Imgs.objects.filter(id=cid, ip_id=page_id).delete()
            data["status"] = True
            data["msg"] = "删除成功！"
        return HttpResponse(json.dumps(data,ensure_ascii=False))
