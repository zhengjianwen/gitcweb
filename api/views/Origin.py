from django.shortcuts import HttpResponse
import json

def Response(request,data,cookies=False):
    obj = HttpResponse(json.dumps(data,ensure_ascii=False))
    # if cookies:
    #     obj.set_cookie("gitcuser",json.dumps(data["data"]["phone"]))
    obj['Access-Control-Allow-Origin'] = 'http://0.0.0.0:3000'
    obj['Access-Control-Allow-Methods'] = str(request.method)
    obj['Access-Control-Allow-Credentials'] = True
    return obj
