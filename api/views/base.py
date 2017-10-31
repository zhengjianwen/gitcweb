from bmpdata.models import Domain
from django.shortcuts import HttpResponse
import json
# 验证token


def datavalidate(func):
    def waper(req,*args,**kwargs):
        token = req.GET.get("token")
        if Domain.objects.filter(token=token).count() == 0:
            return HttpResponse(json.dumps({"status":False,"msg":"不合法的链接！"},ensure_ascii=False))
        ret = func(req,*args,**kwargs)
        return ret
    return waper
