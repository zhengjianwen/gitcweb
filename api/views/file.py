from django.views.decorators.csrf import csrf_exempt
from api.views.Origin import Response
from api.views.base import datavalidate
from bmpdata.models import Files,Library


@datavalidate
@csrf_exempt
def get_file_list(req,library_id):
    data = {"status": False, "msg": None, "data": None}
    if Library.objects.filter(id=library_id).count() != 0:
        a_list = Files.objects.filter(fl__id=library_id).order_by("-weight").values()
        data['data'] = list(a_list)
        data['status'] = True
    else:
        data["msg"] = "传入值不正确！"
    return Response(req, data)

