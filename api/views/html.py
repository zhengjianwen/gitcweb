from django.views import View
from django.shortcuts import HttpResponse,redirect,render
from bmpdata.models import *
from api.views.Origin import Response
import json

class HtmlApiView(View):
    def get(self, request, doman_id,page_id, library_id):
        data = {'status': True, 'data': None}
        try:
            token = request.GET.get('token')
            doman = Domain.objects.filter(id=doman_id, token=token).first()
            if doman:
                title = request.GET.getlist('title', [])
                if not title:
                    dic = list(Html.objects.filter(hp_id=page_id, hl_id=library_id).values('name', 'html'))
                else:
                    dic = list(Html.objects.filter(ap_id=page_id, al_id=library_id).values(*title))
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
