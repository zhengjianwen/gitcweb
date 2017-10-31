from django.shortcuts import render, redirect
from gitc.views.baseview import BaseView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Domain, Page, Library, Article
from bmpdata.logview import write_log
from gitc.gform import ArticleForm
import time


# 文章管理
class ArticleView(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, library_id, cid):
        domain_list = Domain.objects.all()
        info = {'ap_id': page_id, 'al_id': library_id}
        if page_id:
            page_obj = Page.objects.filter(id=page_id).first()
        else:
            return render('/gitcadmin/index.html')
        if library_id:
            library_obj = Library.objects.filter(id=library_id).first()
        else:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        if int(cid) == 0:
            title = '添加文章'
        else:
            if Article.objects.filter(id=cid).count():
                article_obj = Article.objects.filter(id=cid).first()
                title = '修改[ %s ]文章' % article_obj.name
                info['name'] = article_obj.name
                info['content'] = article_obj.content
                info['author'] = article_obj.author
                info['amount'] = article_obj.amount
                info['summary'] = article_obj.summary
            else:
                title = '添加文章'
        obj = ArticleForm(initial=info)
        return render(request, 'tmp/articledit.html', locals())

    @method_decorator(login_required())
    def post(self, request, page_id, library_id, cid):
        ap_id = request.POST.get('ap_id')
        al_id = request.POST.get('al_id')
        self.error = []
        if ap_id != page_id and al_id != library_id:
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
            obj, status = self.creat(request, doman)
        else:
            obj, status = self.edit(request, cid, doman)
        if status:
            return redirect('/gitcadmin/page/%s/index.html' % page_id)
        return render(request, 'tmp/articledit.html', locals())

    def creat(self, request, doman):
        status = True
        obj = ArticleForm(request.POST, request.FILES, status=1)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'], doman, 'article')
                del obj.cleaned_data['img']
            obj.cleaned_data['ctime']= str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))
            a = Article.objects.create(**obj.cleaned_data)
            if not a:
                status = False
                self.error.append({'msg': '数据创建失败'})
        else:
            status = False
            self.error.append({'msg': '数据验证不通过！'})
        return obj, status

    def edit(self, request, cid, doman):
        obj = ArticleForm(request.POST, request.FILES)
        if obj.is_valid():
            if obj.cleaned_data.get('img'):
                obj.cleaned_data['img'] = self.upimg(obj.cleaned_data['img'], doman, 'article')
            else:
                del obj.cleaned_data['img']
            ret = Article.objects.filter(id=cid).update(**obj.cleaned_data)
            status = True if ret else  False

        return obj, status


class ArticleDel(BaseView):
    @method_decorator(login_required())
    def get(self, request, page_id, cid):
        if Article.objects.filter(id=cid, ap_id=page_id).count():
            Article.objects.filter(id=cid, ap_id=page_id).delete()
        return redirect('/gitcadmin/page/%s/index.html' % page_id)
