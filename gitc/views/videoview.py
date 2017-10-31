from django.shortcuts import render, redirect
from gitc.views.baseview import BaseView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Domain, Page, Library, Video
from bmpdata.logview import write_log
from gitc.gform import VideoForm
import time

# 视频管理系统
class VideoView(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'vp_id': page_id, 'vl_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加视频'
        else:
            if Video.objects.filter(id=cid).count():
                video_obj = Video.objects.filter(id=cid).first()
                title = '修改[ %s ] 视频' % video_obj.name
                info['name'] = video_obj.name
                info['url'] = video_obj.url
            else:
                title = '添加视频'
        obj = VideoForm(initial=info)
        return render(request, 'tmp/videoedit.html', locals())

    @method_decorator(login_required())
    def post(self, request, page_id, library_id, cid):
        vp_id = request.POST.get('vp_id')
        vl_id = request.POST.get('vl_id')
        self.error = []
        if vp_id != page_id and vl_id != library_id:
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
            video_obj = Video.objects.filter(id=cid).first()
            obj, status = self.edit(request, cid)
        if status:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request, 'tmp/videoedit.html', locals())

    def creat(self, request):
        status = True
        obj = VideoForm(request.POST, status=1)
        if obj.is_valid():
            obj.cleaned_data['ctime'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            a = Video.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '数据验证失败！'})
        return obj, status

    def edit(self, request, cid):
        obj = VideoForm(request.POST)
        if obj.is_valid():
            ret = Video.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else False
        return obj, status

# 视频删除
class VideoDel(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, cid):
        if Video.objects.filter(id=cid, vp_id=page_id).count():
            Video.objects.filter(id=cid, vp_id=page_id).delete()
        return redirect('/gitcadmin/page/%s/index.html' % page_id)