from webserver.settings import IMGPATH, UPKEY, BASE_DIR
from django.views import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.views.Origin import Response
from api.views.base import datavalidate
from bmpdata.models import Imgs, Domain, Library, Page
import json, time, hashlib, os


class ImgApiView(View):
    def get(self, request, doman_id, page_id, library_id):
        data = {'status': True, 'data': None, 'msg': ''}
        try:
            token = request.GET.get('token')
            doman = Domain.objects.filter(id=doman_id, token=token).first()
            if doman:
                title = request.GET.getlist('title', [])
                if not title:
                    dic = list(
                        Imgs.objects.filter(ip_id=page_id, il_id=library_id).values('title', 'content', 'url', 'img'))
                else:
                    dic = list(Imgs.objects.filter(ip_id=page_id, il_id=library_id).values(*title))
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
        return HttpResponse(json.dumps(data, ensure_ascii=False))


class ImgView(object):
    def __init__(self, request, pid):
        self.t = float(request.POST.get('t', 0))
        self.tn = time.time()
        self.k = UPKEY
        self._pid = pid
        self.token = request.POST.get('token')
        self.file = request.FILES.get('file')
        self.path = IMGPATH % (BASE_DIR, pid)

    def recv(self):
        if self.file:
            filename = self.file.name
            img_path = os.path.join(self.path, filename)
            with open(img_path, 'wb') as f:
                for data in self.file.chunks():
                    f.write(data)
            return '/static/%s/%s' % (self._pid, filename)

    def is_valid(self):
        '''
        数据验证，延时不能超过3秒
        :return:
        '''
        if self.tn - self.t >= 3:
            return False
        m = hashlib.md5()
        data = '%s-%s' % (self.t, self.k)
        m.update(data.encode('utf-8'))
        ret = m.hexdigest()
        if ret != self.token:
            return False
        return True


@csrf_exempt
@datavalidate
def imgup(request, page_id):
    '''内部上传文件接口'''
    status = False
    path = ''
    if request.method == 'POST':
        obj = ImgView(request, page_id)
        if obj.is_valid():
            path = obj.recv()
            if path: status = True
        else:
            status = False
    return HttpResponse(json.dumps({'status': status, 'path': path}))


@datavalidate
@csrf_exempt
def get_img_list(req, library_id):
    data = {"status": False, "msg": "传入值不正确", "data": None}
    order_by = req.GET.get("order_by", "weight")
    if Library.objects.filter(id=library_id).count() > 0:
        a_list = Imgs.objects.filter(il__id=library_id).order_by(order_by).values("url", "title", "content", "weight",
                                                                                  "img")
        l_obj = Library.objects.filter(id=library_id).values("name", "height", "width", "weight", "other")
        data["other"] = list(l_obj)[0]
        data['data'] = list(a_list)
        data['status'] = True
        data["msg"] = "获取成功！"
    return Response(req, data)


@datavalidate
@csrf_exempt
def get_page_img_list(req, page_id):
    data = {"status": False, "msg": "传入值不正确", "data": None}
    order_by = req.GET.get("order_by", "weight")
    if Page.objects.filter(id=page_id).count() > 0:
        tmp_data = []
        # 获取所有的插件列表
        lib_list = list(Library.objects.filter(ptl__page__id=page_id).order_by("weight").values("id", "name", "weight"))
        for l in lib_list:
            tmp = {"title": l["name"], "id": l["id"], "weight": l["weight"], "data": None}
            tmp["data"] = list(Imgs.objects.filter(il__id=l["id"]).order_by(order_by).values("url", "title", "content", "weight", "img"))
            tmp_data.append(tmp)
        data['status'] = True
        data["data"] = tmp_data
        data["msg"] = "获取成功！"
    return Response(req, data)
