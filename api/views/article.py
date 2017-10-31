from django.views import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bmpdata.models import Article,Library,Page
from api.views.base import datavalidate
from api.views.Origin import Response
import json


class ArticleApiView(View):
    def get(self, request,doman_id, page_id, library_id):
        data = {'status': True, 'data': None, 'msg': None}
        try:
            token = request.GET.get('token')
            doman = Domain.objects.filter(id=doman_id, token=token).first()
            if doman:
                title = request.GET.getlist('title', [])
                if not title:
                    dic = list(Article.objects.filter(ap_id=page_id, al_id=library_id).values('name', 'author','img','amount','summary','content'))
                else:
                    dic = list(Article.objects.filter(ap_id=page_id, al_id=library_id).values(*title))
                if not dic:
                    data['msg'] = 'No data'
                else:
                    data['data'] = dic
                    data['parameter'] = list(Library.objects.filter(id=library_id).values('width', 'height'))[0]
            else:
                data['status'] = False
                data['msg'] = 'Validation failure'
        except Exception as e:
            data['status'] = False
            data['msg'] = 'God must be joking'
        return HttpResponse(json.dumps(data,ensure_ascii=False))


@datavalidate
@csrf_exempt
def getarticlelist(req,library_id):
    '''
    获取所有的新闻信息
    :param req:
    :param page_id:
    :return:
    '''
    data = {"status":False,"msg":None,"data":None}
    if Library.objects.filter(id=library_id).count() != 0:
        a_list = Article.objects.filter(al__id=library_id).order_by("-weight").values()
        data['data'] = list(a_list)
        data['status'] = True
    else:
        data["msg"] = "传入值不正确！"
    return Response(req,data)


@datavalidate
@csrf_exempt
def getarticle(req,cid):
    '''
    获取单条新闻
    :param req:
    :param cid: 新闻id号
    :return:
    '''
    data = {"status": False, "msg": None, "data": None}
    if Article.objects.filter(id=cid).count() == 1:
        data['data'] = Article.objects.filter(id=cid).values()[0]
        data["status"] = True
        nub = int(data['data']["amount"]) + 1
        Article.objects.filter(id=cid).update(**{"amount":nub})
    else:
        data["msg"] = '传入值不正确!'
    return Response(req,data)


