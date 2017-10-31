from django.shortcuts import render, redirect,HttpResponse
from gitc.views.baseview import BaseView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Domain, Page, Library, Files
from bmpdata.logview import write_log
from gitc.gform import FileForm
import json,time

# 文件管理
class AddFileView(BaseView):

    @method_decorator(login_required)
    def get(self,request,page_id,library_id):
        domain_list = Domain.objects.all()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        obj = FileForm(initial={"fp_id":page_id,"fl_id":library_id})
        return render(request,'tmp/fileedit.html',locals())

    @method_decorator(login_required)
    def post(self, request,page_id,library_id):
        domain_list = Domain.objects.all()
        fp_id = request.POST.get('fp_id')
        fl_id = request.POST.get('fl_id')
        if fp_id != page_id and fl_id != library_id:
            doman = Domain.objects.filter(pagetemplate__library__id=library_id).first()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
            doman = Domain.objects.filter(pagetemplate__page=page_obj).first()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        obj = FileForm(request.POST,request.FILES)
        if obj.is_valid():
            file = request.FILES.get('url')
            obj.cleaned_data["url"] = self.upimg(file,doman,"file")
            obj.cleaned_data['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            Files.objects.create(**obj.cleaned_data)
            return redirect("/gitcadmin/page/%s/index.html" % page_id)
        return render(request, 'tmp/fileedit.html', locals())


class EditFileView(BaseView):

    @method_decorator(login_required)
    def get(self, request, page_id, library_id,cid):
        domain_list = Domain.objects.all()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        data = Files.objects.filter(id=cid).values().first()
        if not data:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        obj = FileForm(initial=data)
        return render(request, 'tmp/fileedit.html', locals())

    @method_decorator(login_required)
    def post(self, request, page_id, library_id,cid):
        domain_list = Domain.objects.all()
        fp_id = request.POST.get('fp_id')
        fl_id = request.POST.get('fl_id')
        doman = None
        if fp_id != page_id and fl_id != library_id:
            doman = Domain.objects.filter(pagetemplate__library__id=library_id).first()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
            doman = Domain.objects.filter(pagetemplate__page=page_obj).first()
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        fobj = Files.objects.filter(id=cid).first()
        obj = FileForm(request.POST, request.FILES)
        if not fobj:
            return render(request, 'tmp/fileedit.html', locals())
        if obj.is_valid() and doman:
            file = request.FILES.get('url')
            obj.cleaned_data["url"] = self.upimg(file, doman, "file")
            Files.objects.filter(id=cid).update(**obj.cleaned_data)
            return redirect("/gitcadmin/page/%s/index.html" % page_id)
        return render(request, 'tmp/fileedit.html', locals())


# 文件下载
class delFile(BaseView):

    def get(self,request,page_id, library_id,cid):
        data = {"status":True,"data":None,"msg":None}

        return HttpResponse(json.dumps(data))