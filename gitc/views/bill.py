from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from webserver.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bmpdata.models import Domain, Bill,Memberinfo,Ticket
from gitc.views.utils import Export_data
from gitc.gform import BillForm,MemberForm
import json,time,os,xlrd,random,re


class BillView(View):

    @method_decorator(login_required)
    def get(self,req):
        domain_list = Domain.objects.all()
        data = Bill.objects.all()
        return render(req,"admin/bill.html",locals())


class BillEdit(View):

    @method_decorator(login_required)
    def get(self,req,cid):
        domain_list = Domain.objects.all()
        if Bill.objects.filter(id=cid).count() != 0:
            bill_obj = Bill.objects.filter(id=cid)
            bill_dic = bill_obj.values()[0]
            member_obj = Memberinfo.objects.filter(phone=bill_dic["phone"]).values().first()
            uobj = MemberForm(initial=member_obj)
            obj = BillForm(initial=bill_dic)
        else:
            error = "没有此条信息！"
        return render(req, "admin/billedit.html", locals())

    @method_decorator(login_required)
    def post(self,req,cid):
        domain_list = Domain.objects.all()
        if Bill.objects.filter(id=cid).count() != 0:
            uobj = MemberForm(req.POST)
            obj = BillForm(req.POST)
            if uobj.is_valid() and obj.is_valid():
                bill = Bill.objects.filter(id=cid).values().first()
                member = Memberinfo.objects.filter(phone=bill["phone"]).values().first()
                u_dic = self.makedata(uobj.cleaned_data,member)
                b_dic = self.makedata(obj.cleaned_data,bill)
                Bill.objects.filter(id=cid).update(**b_dic)
                Memberinfo.objects.filter(phone=bill["phone"]).update(**u_dic)
                print(u_dic,b_dic)
            else:
                error = "%s<br>%s"%(uobj.errors,uobj.errors)
                return render(req, "admin/billedit.html", locals())
        return redirect('/gitcadmin/bill.html')

    def makedata(self,dic,old_data):
        tmp = {}
        for k,v in dic.items():
            if str(v).strip() != "" and v != old_data[k]:
                if k == "sex":
                    try:
                        v = int(v)
                    except Exception as e:
                        v = 0
                tmp[k] = v
        return tmp


class BillUpXls(View):

    @method_decorator(login_required)
    def get(self, req,domain_id):
        domain_list = Domain.objects.all()
        return render(req, "admin/importbill.html", locals())

    @method_decorator(login_required)
    def post(self,req,domain_id):
        '''上传文件'''
        domain_list = Domain.objects.all()
        path = self._recv(req)
        domain = Domain.objects.filter(id=domain_id)
        ticket_list = list(Ticket.objects.filter(td__id=domain_id).values("id","name","code"))
        if path:
            data = self._readxls(path,ticket_list,domain_id)
        else:
            data = []
        return render(req, "admin/importbill.html", locals())

    def _recv(self,req):
        file = req.FILES.get("file")
        if file:
            _, hz = str(file.name).rsplit('.', 1)
            filename = 'tmp20170921.%s' %  hz
            file_path = os.path.join(BASE_DIR, filename)
            with open(file_path, 'wb') as f:
                for data in file.chunks():
                    f.write(data)
            return file_path

    def _readxls(self,path,ticket_list,domain_id):
        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        title = ['order_time', 'order_nub', 'bt_id', 'price', 'code', 'name', 'email', "phone",'company', 'position', 'age',
                 'channel', 'channel_code',"sign_staus","remarks"]
        data = []
        ticket = [t["name"] for t in ticket_list]
        for i in range(nrows):
            # 获取每行数据
            row_val = table.row_values(i)
            if i == 0:
                continue
            tmp = {'status': False, 'data': {},"msg":None}
            # 将值变成键值对的方式保存
            for index, key in enumerate(title):
                val = row_val[index]
                if key == "bt_id" and val in ticket:
                    tmp['data']["ticket"] = val
                    val = ticket_list[ticket.index(val)]["id"]
                elif key == "code":
                    val = self._makecode(tmp['data']["bt_id"],ticket_list)
                elif key == "phone":
                    val = str(row_val[index])[:11]
                elif key == "age":
                    val = int(row_val[index])
                tmp['data'][key] = val
                tmp['data']["bd_id"] = domain_id
            # 数据验证
            if self.is_valid(tmp['data']):
                tmp['status'] = True
            data.append(tmp)
        os.remove(path)
        return data

    def _makecode(self,bt_id,ticket_list):
        """创建code"""
        code = "{y}{m}{d}{random|8}"
        for dic in ticket_list:
            if dic["id"] == bt_id:
                code = dic["code"]
                break
        dic = {"m": "01", "d": "01", "y": "2017", "readm": "808"}
        dic["y"] = str(time.strftime("%Y", time.gmtime()))
        dic["d"] = str(time.strftime("%d", time.gmtime()))
        dic["m"] = str(time.strftime("%m", time.gmtime()))
        randomnub = code.count("random")
        randomkey = re.findall(r"random\|\d+", code)
        if randomnub == len(randomkey):
            for key in randomkey:
                _, nub = key.split("|")
                tmp = ""
                for i in range(int(nub)):
                    if i == 0:
                        tmp += str(random.randint(1, 9))
                    else:
                        tmp += str(random.randint(0, 9))
                dic[key] = tmp
        return code.format(**dic)

    def is_valid(self,data):
        m_obj = MemberForm(data)
        b_obj = BillForm(data)
        if m_obj.is_valid() and b_obj.is_valid():
            return True
        return False


class BillAdd(View):

    @method_decorator(login_required)
    def post(self,req):
        data = {"status":True,"msg":""}
        m_obj = MemberForm(req.POST)
        b_obj = BillForm(req.POST)
        if m_obj.is_valid() and b_obj.is_valid():
            if Memberinfo.objects.filter(phone=m_obj.cleaned_data["phone"]).count() != 0:
                Memberinfo.objects.filter(phone=m_obj.cleaned_data["phone"]).update(**m_obj.cleaned_data)
            else:
                Memberinfo.objects.create(**m_obj.cleaned_data)
            Bill.objects.create(**b_obj.cleaned_data)
        else:
            data["status"] = False
            data["msg"] = "创建失败"
        return HttpResponse(json.dumps(data,ensure_ascii=False))


@login_required
def make_excel_bill(req,bid):
    data = {"status": True, "msg": "生成成功","url":None}
    tmp = {"phone":"手机号","code":"票号","name":"姓名","order_time":"订单时间","order_nub":"订单号","bt__name":"票名称","price":"价格",
           "channel":"渠道","channel_code":"渠道编码","sign_staus":"签到状态","sign_time":"签到时间"}
    keys = req.GET.getlist("keys")
    if not keys:
        keys = [key for key in tmp]
    keys = sorted(keys)
    title = [tmp.get(key,key) for key in keys]
    bill_list = Bill.objects.filter(bd=bid).values(*keys)
    obj = Export_data(bill_list,keys,title)
    url = obj.down_url()
    data["status"] = True if url else False
    data["msg"] = "生成成功！" if url else "生成失败！"
    data["url"] = url
    return HttpResponse(json.dumps(data, ensure_ascii=False))

@login_required
def del_bill(req, bid):
    data = {"status": True, "msg": "删除成功"}
    if not Bill.objects.filter(id=bid).delete():
        data["status"] = False
        data["msg"] = "删除失败!"
    return HttpResponse(json.dumps(data, ensure_ascii=False))
