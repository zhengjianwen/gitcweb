from django.template import Library
from django.utils.safestring import mark_safe
from bmpdata.models import Imgs
register = Library()

@register.simple_tag
def getpicnub(obj):
    nub = Imgs.objects.filter(orgid__meet=obj).count()
    return nub

@register.simple_tag
def makenub(status):
    if not status:
        return 0
    return 1


@register.simple_tag
def showdata(data,nub):
    if len(data) > nub:
        return mark_safe(data[:nub])
    else:
        return mark_safe(data)

@register.simple_tag
def getpersonstyle(nub):
    if nub//2 == 0:
        html = '<tr class="even pointer" status="0">'
    else:
        html = '<tr class="odd pointer" status="0">'
    return mark_safe(html)

@register.simple_tag
def splitstr(data):
    return data[:7]
