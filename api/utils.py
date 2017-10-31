import requests, random, redis, json, os, hashlib, uuid
from webserver.settings import SMS_ID, SMS_KEY, SMS_URL, REDIS_ADDR, REDIS_PORT, BASE_DIR,REDIS_TIME,REDIS_PASW,REDIS_DB,EMAIL_HOST_USER
from django.core.mail import send_mail
from barcode.writer import ImageWriter
from barcode.codex import Code39

class Myredis(object):

    def __init__(self,redis_db=REDIS_DB):
        pool = redis.ConnectionPool(host=REDIS_ADDR, port=REDIS_PORT, db=redis_db)
        self.r = redis.Redis(connection_pool=pool)

    def set(self, phone, code):
        self.r.set(phone, code, REDIS_TIME)
        self.r.save()

    def login(self,phone):
        self.r.set(phone,1,60*12*7)
        self.r.save()

    def islogin(self,phone):
        if self.get(phone):
            return True
        return False

    def exists(self, phone):
        return self.r.exists(phone)

    def get(self, phone):
        return self.r.get(phone)

    def delete(self,phone):
        return self.r.delete(phone)

myredis = Myredis()


class Sms(object):
    #  发送短信
    def sendsms(self, phone):
        data = {"status":True,"msg":None}
        if myredis.exists(phone):  # 验证是否发送没有验证！
            data["msg"] = "验证码已经发送，请稍后再试！"
            data["status"] = False
            return data
        code = self._code()  # 获取验证码
        conten = "欢迎注册登录GITC，您的验证码是 %s ,请在页面中填写验证码完成验证，有效期3分钟。" % code
        post_data = {"account": SMS_ID,
                "password": SMS_KEY,
                "mobile": phone,
                "content": conten,
                "format": "json"
                }
        ret = requests.post(SMS_URL, post_data)
        ret = json.loads(ret.text)
        if ret["code"] == 2:
            myredis.set(str(phone).strip(), code)  # 存储验证码
            data["msg"] = "发送成功"
            data["status"] = True
        else:
            data["msg"] = "发送失败！您发送次数过多！"
            data["status"] = False
        return data

    def _code(self):
        code = ""
        for i in range(4):
            if i == 0 :
                code += str(random.randint(1, 9))
            else:
                code += str(random.randint(0, 9))
        return int(code)


def validatecode(phone, code):
    '''验证验证码是否正确'''
    if not phone or not code:
        return False
    tmp =myredis.get(phone)
    if str(code).encode("utf-8") == tmp:
        myredis.delete(phone)
        return True
    else:
        return False


def validatephone(phone):
    '''
    验证手机号
    移动号码段:139、138、137、136、135、134、150、151、152、157、158、159、182、183、187、188、147
    联通号码段:130、131、132、136、185、186、145
   电信号码段:133、153、180、189
    :param phone:
    :return:
    '''
    phone = str(phone).strip()
    data = ["139","138","137","136","135","134","150","151","152","157","158","159","182","183","187","188",
            "147","130","131","132","136","185","186","145","133","153","180","189"]
    try:
        if phone[:3] in data:
            return False
        if len(phone) != 11:
            return False
        if str(phone).isdigit():
            return True
    except Exception as e:
        return False


def md5(data=None):
    if not data:
        data = str(uuid.uuid1()).encode('utf-8')
    m = hashlib.md5()
    m.update(data)
    return str(m.hexdigest())


def recvimg(file):
    _, hz = str(file.name).rsplit(".", 1)
    filename = "%s.%s" % (md5(), hz)
    path = os.path.join(BASE_DIR, "static", "upload", filename)
    with open(path, "wb") as f:
        for data in file.chunks():
            f.write(data)
    return "static/upload/%s" % filename




def send_self_mail(title,data):
    ret = send_mail(title, data,EMAIL_HOST_USER,['gitc@kylinclub.org'], fail_silently=True)
    return True if ret else False


def generagteBarCode(data):
        imagewriter = ImageWriter()
        #保存到图片中
        # add_checksum : Boolean   Add the checksum to code or not (default: True)
        ean = Code39(data, writer=imagewriter, add_checksum=False)
        # 不需要写后缀，ImageWriter初始化方法中默认self.format = 'PNG'
        ean.save('image2')
