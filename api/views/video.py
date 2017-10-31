from webserver.settings import TOKEN, UPPORT, UPURL, IMGPATH, UPKEY,BASE_DIR
from django.views import View
from django.shortcuts import HttpResponse,redirect,render
from django.views.decorators.csrf import csrf_exempt
from bmpdata.models import *
from api.views.Origin import Response
import json, time, hashlib, os


class VideoApiView(View):

    def get(self, request,doman_id, page_id, library_id):
        data = {'status': True, 'data': None,'msg':None}
        try:
            token = request.GET.get('token')
            doman = Domain.objects.filter(id=doman_id, token=token).first()
            if doman:
                title = request.GET.getlist('title', [])
                if not title:
                    dic = list(Video.objects.filter(vp_id=page_id, vl_id=library_id).values('name', 'url'))
                else:
                    dic = list(Video.objects.filter(vp_id=page_id, vl_id=library_id).values(*title))
                if not dic:
                    data['msg'] = 'No data！'
                else:
                    data['data'] = dic
                    data['parameter'] = list(Library.objects.filter(id=library_id).values('width', 'height'))[0]
            else:
                data['status'] = False
                data['msg'] = 'Validation failure'
        except Exception as e:
            data['status'] = False
            data['msg'] = 'God must be joking'
        return Response(request,data)