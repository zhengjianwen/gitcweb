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
from gitc.views import basics,logic,imgview,personview,articleview,htmlview,videoview,fileview,infoview,ticket,bill

urlpatterns = [
    url(r'^index.html$', basics.indexview),
    url(r'^login.html$', basics.loginview),
    url(r'^logout.html$', basics.logoutview),
    url(r'^changepwd.html$', basics.changepwd),
    url(r'^domain/index.html$', logic.DomainView.as_view()),

    url(r'^library/index.html$', logic.LibraryView.as_view()),
    url(r'^library/del/(?P<cid>\d+)$', logic.LibraryDel.as_view()),

    url(r'^page/index.html$', logic.PageView.as_view()),
    url(r'^page/del/(?P<cid>\d+)$', logic.PageDel.as_view()),

    url(r'^template/index.html$', logic.TemplateView.as_view()),
    url(r'^template/del/(?P<cid>\d+)$', logic.TemplateDel),
    # 加入我们
    url(r'^contact.html$', infoview.contact),
    url(r'^sponsor.html$', infoview.sponsorlist),
    url(r'^sponsor/del/(?P<cid>\d+)$', infoview.delsponsor),
    url(r'^sponsor/excel/(?P<bid>\d+)$', infoview.make_excel_sponsor),

    url(r'^memberlist.html$', infoview.menmberlist),
    url(r'^member/del/(?P<cid>\d+)$', infoview.delmenber),
    url(r'^member/edit/(?P<cid>\d+)$', infoview.MemberEdita.as_view()),
    url(r'^member/excel/(?P<bid>\d+)$', infoview.make_excel_menber),

    url(r'^meetissue.html$', infoview.meetissuelist),
    url(r'^meetissue/del/(?P<cid>\d+)$', infoview.delmeetissue),
    url(r'^meetissue/excel/(?P<bid>\d+)$', infoview.make_excel_meetissue),

    url(r'^bill.html$', bill.BillView.as_view()),
    url(r'^bill/(?P<cid>\d+)/edit.html$', bill.BillEdit.as_view()),
    url(r'^bill/del/(?P<bid>\d+)$', bill.del_bill),
    url(r'^bill/excel/(?P<bid>\d+)$', bill.make_excel_bill),
    url(r'^bill/(?P<domain_id>\d+)/upload.html$', bill.BillUpXls.as_view()),
    url(r'^bill/add.html$', bill.BillAdd.as_view()),
    url(r'^u/del/(?P<cid>\d+)$', basics.delcontact),

    url(r'^page/add.html$', logic.Addpage.as_view()),

    url(r'^page/(?P<cid>\d+)/index.html$', logic.UPageView.as_view()),

    url(r'^img-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', imgview.ImgView.as_view()),
    url(r'^img/(?P<page_id>\d+)/del/(?P<cid>\d+)$', imgview.ImgDel.as_view()),
    url(r'^article-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', articleview.ArticleView.as_view()),
    url(r'^article/(?P<page_id>\d+)/del/(?P<cid>\d+)$', articleview.ArticleDel.as_view()),
    url(r'^personnel-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', personview.PersonnelView.as_view()),
    url(r'^personnel/(?P<page_id>\d+)/del/(?P<cid>\d+)$', personview.PersonnelDel.as_view()),
    url(r'^personnel-(?P<page_id>\d+)/(?P<library_id>\d+)/import.html$', personview.ImportPerson.as_view()),
    url(r'^personnel/add/person$', personview.PersonAddAjax),
    url(r'^del/person/(?P<cid>\d+)$', personview.PersonDelAjax),

    url(r'^html-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', htmlview.HtmlView.as_view()),
    url(r'^html/(?P<page_id>\d+)/del/(?P<cid>\d+)$', htmlview.HtmlDel.as_view()),
    url(r'^video-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', videoview.VideoView.as_view()),
    url(r'^video/(?P<page_id>\d+)/del/(?P<cid>\d+)$', videoview.VideoDel.as_view()),
    url(r'^kindeditor/upload.html$', logic.upload_kindeditor_img),

    url(r'^eamil-type/index.html$', logic.MailTypeView.as_view()),
    url(r'^email/index.html$', logic.Mail.as_view()),

    url(r'^ticket/index.html$', ticket.TicketView.as_view()),
    url(r'^ticket/edit/index.html$', ticket.TicketEdit.as_view()),


    url(r'^file-(?P<page_id>\d+)/(?P<library_id>\d+)/add/0$', fileview.AddFileView.as_view()),
    url(r'^file-(?P<page_id>\d+)/(?P<library_id>\d+)/edit/(?P<cid>\d+)$', fileview.EditFileView.as_view()),
    # url(r'', basics.indexview),

]
