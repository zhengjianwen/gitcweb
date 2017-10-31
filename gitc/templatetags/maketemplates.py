from django.template import Library as li
from django.shortcuts import render
from django.utils.safestring import mark_safe
from webserver.settings import APIURL
from bmpdata.models import *

register = li()


@register.simple_tag
def makeimg(request, page_id, library_id, name):
    data_list = Imgs.objects.filter(ip_id=page_id, il_id=library_id).order_by("-weight")
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/img/%s-%s-%s.json' % (APIURL,library_obj.ptl_id, page_id, library_id)
    html = render(request, 'tmp/imgs.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makevideo(request, page_id, library_id, name):
    data_list = Video.objects.filter(vp_id=page_id, vl_id=library_id).order_by("-weight")
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/video/%s-%s-%s.json' % (APIURL, library_obj.ptl_id, page_id, library_id)
    html = render(request, 'tmp/video.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makearticle(request, page_id, library_id, name):
    data_list = Article.objects.filter(ap_id=page_id, al_id=library_id).order_by("-weight")
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/article/%s-%s-%s.json' % (APIURL, library_obj.ptl_id, page_id, library_id)
    html = render(request, 'tmp/article.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makepersonnel(request, page_id, library_id, name):
    data_list = Personnel.objects.filter(ppl_id=page_id, pl_id=library_id).order_by("-weight")
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/person/%s-%s-%s.json' % (APIURL, library_obj.ptl_id, page_id, library_id)
    html = render(request, 'tmp/personnel.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makehtml(request, page_id, library_id, name):
    data_list = Html.objects.filter(hp_id=page_id, hl_id=library_id).order_by("-weight")
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/other/%s-%s-%s.json' % (APIURL, library_obj.ptl_id, page_id, library_id)
    html = render(request, 'tmp/html.html', locals())
    return mark_safe(html.content)


@register.simple_tag
def makefile(request, page_id, library_id, name):
    data_list = Files.objects.filter(fp_id=page_id, fl_id=library_id).order_by("-weight")
    library_obj = Library.objects.filter(id=library_id).first()
    api = '%s/api/file/%s-%s-%s.json' % (APIURL, library_obj.ptl_id, page_id, library_id)
    html = render(request, 'tmp/file.html', locals())
    return mark_safe(html.content)

###################################

@register.simple_tag
def bt(meet):
    html = '<li><a><i class="fa fa-desktop"></i>%s<span class="fa fa-chevron-down"></span></a>'
    nub = Page.objects.filter(pp__domain=meet).count()
    html = html % meet.name if nub else ''
    return mark_safe(html)

@register.simple_tag
def domain_page(obj):
    return Page.objects.filter(pp__domain=obj).count()

@register.simple_tag
def domain_tp(obj):
    return PageTemplate.objects.filter(domain=obj).count()

@register.simple_tag
def getl_to_tp(obj):
    return obj.ptl_set.all().count()

@register.simple_tag
def makename(user):
    lname = user.last_name
    if lname != "":
        fname = user.first_name
        name = "%s%s"%(lname,fname)
    else:
        name = user.username
    return name