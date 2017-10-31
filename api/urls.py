"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.shortcuts import HttpResponse
from api.views import person,other,video,img,article,user,html,file

def error(request):
    return HttpResponse('404')

urlpatterns = [
    url(r'^img/(?P<doman_id>\d+)-(?P<page_id>\d+)-(?P<library_id>\d+).json$', img.ImgApiView.as_view()),
    url(r'^gitc/img-(?P<library_id>\d+)/list.json$', img.get_img_list),
    url(r'^gitc/page/img-(?P<page_id>\d+)/list.json$', img.get_page_img_list),

    url(r'^video/(?P<doman_id>\d+)-(?P<page_id>\d+)-(?P<library_id>\d+).json$', video.VideoApiView.as_view()),

    url(r'^article/(?P<doman_id>\d+)-(?P<page_id>\d+)-(?P<library_id>\d+).json$', article.ArticleApiView.as_view()),
    url(r'^gitc/article-(?P<library_id>\d+)/list.json$', article.getarticlelist),
    url(r'^gitc/article/(?P<cid>\d+).json$', article.getarticle),

    # url(r'^person/(?P<doman_id>\d+)-(?P<page_id>\d+)-(?P<library_id>\d+).json$', person.PersonApiView.as_view()),
    url(r'^gitc/person-(?P<library_id>\d+)/list.json$', person.personlist),
    url(r'^gitc/person-(?P<page_id>\d+)/all/list.json$', person.page_person),
    url(r'^gitc/person/(?P<pid>\d+).json$', person.person),

    url(r'^other/(?P<doman_id>\d+)-(?P<page_id>\d+)-(?P<library_id>\d+).json$', html.HtmlApiView.as_view()),

    url(r'^gitc/user/(?P<phone>\d+).json$', user.userlogin),
    url(r'^gitc/code/(?P<phone>\d+).json$', user.sendsms),
    # 用户收藏信息
    url(r'^gitc/collect/(?P<phone>\d+).json$', user.getmycollect),
    url(r'^gitc/collect/add/(?P<phone>\d+).json$', user.add_user_collect),
    url(r'^gitc/file/(?P<phone>\d+).json$', user.user_file_collect),
    # 用户票务
    url(r'^gitc/tricket/list/(?P<phone>\d+).json$', user.user_tricket_list),
    url(r'^gitc/tricket/(?P<phone>\d+).json$', user.user_tricket),

    # 下载列表
    url(r'^gitc/file-(?P<library_id>\d+)/list.json$', file.get_file_list),

    url(r'^gitc/file/add/(?P<phone>\d+).json$', user.add_user_file),
    # 用户
    url(r'^gitc/sponsor/add.json$', other.sponsor_add),
    url(r'^gitc/meetissue/add.json$', other.meetissue_add),
    url(r'^gitc/meetissue/upload.json$', other.meetissue_upload),
    url(r'^contact/add.html$', other.ContactApiView),
    url(r'^member/logout.html$', user.user_logout),
    # url(r'^imguplod/(?P<page_id>\d+)/uplod.html$', views.imgup),
    #url(r'^update.html$', other.makedata),
    url(r'',error ),
]
