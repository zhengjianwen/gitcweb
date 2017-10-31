from bmpdata.models import *
from django.forms.forms import Form
from django.forms import fields, widgets
from django.core.exceptions import ValidationError
from pypinyin import lazy_pinyin
import uuid, re


class ChangepwdForm(Form):
    oldpassword = fields.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=widgets.PasswordInput(
            attrs={'class': "form-control col-md-7 col-xs-12",
                   'placeholder': u"原密码",
                   }
        ),
    )
    newpassword1 = fields.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=widgets.PasswordInput(
            attrs={'class': "form-control col-md-7 col-xs-12",
                   'placeholder': u"新密码",
                   }
        ),
    )
    newpassword2 = fields.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=widgets.PasswordInput(
            attrs={'class': "form-control col-md-7 col-xs-12",
                   'placeholder': u"确认密码",
                   }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class PageForm(Form):
    pp_id = fields.CharField(widget=widgets.Select())
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True)
    url = fields.CharField(required=False, max_length=64, min_length=1, strip=True)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['pp_id'].widget.choices = PageTemplate.objects.all().values_list('id', 'name')


class ImgsForm(Form):
    ip_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    il_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    title = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "标题名称", 'class': "form-control col-md-7 col-xs-12"}
                             ))
    content = fields.CharField(required=False, widget=widgets.Textarea(
        attrs={'class': 'form-control',
               'placeholder': '请在此填写类型内容，没有请为空。',
               'rows': '10',
               'id': 'mycontent'}))
    url = fields.CharField(required=False, max_length=256, strip=True,
                           widget=widgets.TextInput(
                               attrs={'placeholder': "url地址", 'class': "form-control col-md-7 col-xs-12"}
                           ))
    img = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12", }))
    weight = fields.IntegerField(required=False, initial=1,
                                 widget=widgets.NumberInput(attrs={'class': "form-control col-md-7 col-xs-12"}))

    def clean_img(self):
        img = self.cleaned_data['img']
        # status 1 创建数据
        if self.status and not img:
            raise ValidationError('图片不能为空')
        if img:
            _, ext = str(img.name).rsplit('.', 1)
            if ext not in ('jpg', 'png', 'gif'):
                raise ValidationError('图片格式不正确')
        return img

    def clean_title(self):
        val = self.cleaned_data['title']
        if not val:
            val = '%s' % uuid.uuid1()
        return val[:10]

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get('status', 0)
        if kwargs.get('status'):
            del kwargs['status']
        super(ImgsForm, self).__init__(*args, **kwargs)
        self.fields['ip_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['il_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Imgs


class ArticleForm(Form):
    ap_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    al_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "标题名称", 'class': "form-control col-md-7 col-xs-12"}))
    author = fields.CharField(required=True, max_length=64, min_length=1, strip=True, initial='admin',
                              widget=widgets.TextInput(
                                  attrs={'placeholder': "作者，默认为admin", 'class': "form-control col-md-3 col-xs-3"}))
    amount = fields.IntegerField(required=True, initial=1,
                                 widget=widgets.TextInput(attrs={'class': "form-control col-md-7 col-xs-12"}))
    content = fields.CharField(required=True, widget=widgets.Textarea(
        attrs={'class': 'form-control', 'id': 'mycontent'}))
    summary = fields.CharField(required=False, widget=widgets.Textarea(
        attrs={'class': 'form-control', 'rows': '2',
               'placeholder': '如果为空自动截取文字的前200字。'}))
    img = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12", }))
    weight = fields.IntegerField(required=False, initial=1,
                                 widget=widgets.NumberInput(attrs={'class': "form-control col-md-7 col-xs-12"}))

    def clean(self):
        summary = self.cleaned_data.get('summary')
        if not summary:
            self.cleaned_data['summary'] = self.makedata(self.cleaned_data.get('content'))
        return self.cleaned_data

    def makedata(self, data):
        '''处理内容转换成简介'''
        len_ = re.findall(r'<.+>', data)
        for i in len_:
            data = data.replace(i, '')
        data = data.replace('&nbsp;', '')
        data = data.strip()
        return data[:200]

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get('status', 0)
        if kwargs.get('status'):
            del kwargs['status']
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['ap_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['al_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Article


class PersonnelForm(Form):
    ppl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    pl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "中文名", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    ename = fields.CharField(required=False, max_length=128, min_length=1, strip=True,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "姓名全拼", 'class': "form-control col-md-7 col-xs-12"}
                             ))
    company = fields.CharField(required=True, max_length=128, min_length=1,
                               widget=widgets.TextInput(
                                   attrs={'placeholder': "公司名称", 'class': "form-control col-md-7 col-xs-12"}
                               ))
    position = fields.CharField(required=True, max_length=128, min_length=1,
                                widget=widgets.TextInput(
                                    attrs={'placeholder': "职位名称", 'class': "form-control col-md-7 col-xs-12"}
                                ))
    summary = fields.CharField(required=False, widget=widgets.Textarea(
        attrs={'class': 'form-control',
               'placeholder': '请在此填写人员简介，如无可以不填',
               'rows': '5',
               'id': 'mycontent'}))
    pic = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12"}))
    stheme = fields.CharField(required=False, max_length=128, min_length=1,
                              widget=widgets.TextInput(
                                  attrs={'placeholder': "演讲主题", 'class': "form-control col-md-7 col-xs-12"}
                              ))
    sintroduce = fields.CharField(required=False, widget=widgets.Textarea(
        attrs={'class': 'form-control',
               'placeholder': '请在此填写演讲介绍内容，如无可以不填',
               'rows': '5',
               'id': 'sintroduce'}))
    sdata = fields.CharField(required=False, max_length=128, min_length=1,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "2017-01-01", 'class': "form-control col-md-7 col-xs-12"}
                             ))
    stime = fields.CharField(required=False, max_length=128, min_length=1,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "演讲时间:12：00", 'class': "form-control col-md-7 col-xs-12"}
                             ))
    meet = fields.CharField(required=False, max_length=128, min_length=1,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "专场名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    meetaddr = fields.CharField(required=False, max_length=128, min_length=1,
                                widget=widgets.TextInput(
                                    attrs={'placeholder': "会场地点", 'class': "form-control col-md-7 col-xs-12"}
                                ))
    weight = fields.IntegerField(required=False, initial=1,
                                 widget=widgets.NumberInput(attrs={'class': "form-control col-md-7 col-xs-12"}))

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(PersonnelForm, self).__init__(*args, **kwargs)
        self.fields['ppl_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['pl_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    def clean_pic(self):
        '''判读图片的格式是否正确,判断传入是否是批量上传的数据'''
        val = self.cleaned_data['pic']
        if self.status == 2 or not self.status:
            return val
        if val:
            _, ext = str(val.name).rsplit('.', 1)
            if ext not in ('jpg', 'png', 'gif'):
                raise ValidationError('图片格式不正确')
        else:
            val = ''
        return val

    def clean(self):
        val = lazy_pinyin(self.cleaned_data['name'])
        if not self.cleaned_data['ename']:
            self.cleaned_data['ename'] = ''.join(val)
        if not self.cleaned_data['pic']:
            del self.cleaned_data['pic']
        return self.cleaned_data

    class Meta:
        module = Personnel


class HtmlForm(Form):
    hp_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    hl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "标题必填项", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    html = fields.CharField(required=False, widget=widgets.Textarea(
        attrs={'class': 'form-control',
               'placeholder': '请输入HTML代码！',
               'rows': '10',
               'id': 'mycontent'}))
    weight = fields.IntegerField(required=False, initial=1,
                                 widget=widgets.NumberInput(attrs={'class': "form-control col-md-7 col-xs-12"}))

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(HtmlForm, self).__init__(*args, **kwargs)
        self.fields['hp_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['hl_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Html


class FileForm(Form):
    fp_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    fl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    user_id = fields.CharField(required=False,
                               widget=widgets.Select(attrs={'class': "form-control col-md-7 col-xs-12"}))
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "地址名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    url = fields.CharField(required=True, widget=widgets.FileInput(attrs={'class': 'form-control'}))
    weight = fields.IntegerField(required=False, initial=1,
                                 widget=widgets.NumberInput(attrs={'class': "form-control col-md-7 col-xs-12"}))

    def __init__(self, *args, **kwargs):
        fp_id = kwargs.get("fp_id", 0)
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0

        if kwargs.get('status'):
            del kwargs['status']
        super(FileForm, self).__init__(*args, **kwargs)
        if fp_id:
            self.fields['user_id'].widget.choices = Personnel.objects.filter(ppl_id=fp_id).values_list('id', 'name')
        else:
            self.fields['user_id'].widget.choices = Personnel.objects.values_list('id', 'name')
        self.fields['fp_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['fl_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Files


class VideoForm(Form):
    vp_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    vl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "hide"}))
    name = fields.CharField(required=True, max_length=128, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "视频名称为必填项", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    url = fields.CharField(required=True, widget=widgets.TextInput(
        attrs={'placeholder': "url地址，后缀为：swf...", 'class': "form-control col-md-7 col-xs-12"}))
    weight = fields.IntegerField(required=False, initial=1,
                                 widget=widgets.NumberInput(attrs={'class': "form-control col-md-7 col-xs-12"}))

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'):
            del kwargs['status']
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['vp_id'].widget.choices = Page.objects.all().values_list('id', 'name')
        self.fields['vl_id'].widget.choices = Library.objects.all().values_list('id', 'name')

    class Meta:
        module = Video


class DomainForm(Form):
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "网站名称，必填项", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    url = fields.URLField(required=True, max_length=64, min_length=1, strip=True,
                          widget=widgets.URLInput(
                              attrs={'placeholder': "网站链接，点击后可以跳转的页面。", 'class': "form-control col-md-7 col-xs-12"}
                          ))
    imgpath = fields.CharField(required=True, max_length=128, strip=True, initial="/data_new/",
                               widget=widgets.TextInput(
                                   attrs={'placeholder': "请填写服务器图片存放的物理路径！", 'class': "form-control col-md-7 col-xs-12"}
                               ))

    def clean(self):
        '''验证数据是否重复'''
        name = self.cleaned_data.get('name')
        ret = Domain.objects.filter(name=name).count()
        if self.status and ret:
            del self.cleaned_data['name']
        else:
            if ret:
                raise ValidationError('数据重复')
        return self.cleaned_data

    def __init__(self, status=0, *args, **kwargs):
        # try:
        #     self.status = kwargs.get('status', 0)
        #     if kwargs.get('status'):
        #         del kwargs['status']
        # except Exception as e:
        #     self.status = 0
        # if kwargs.get('status'):
        #     del kwargs['status']
        super(DomainForm, self).__init__(*args, **kwargs)

    class Meta:
        module = Domain


class LibraryForm(Form):
    ptl_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    plugin_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    weight = fields.CharField(required=False, initial=1,
                              widget=widgets.NumberInput(attrs={'class': "form-control col-md-6 col-xs-6"}))
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "模板名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    width = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "容许多宽？不填默认100%", 'class': "form-control col-md-7 col-xs-12"}
                             ))
    height = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                              widget=widgets.TextInput(
                                  attrs={'placeholder': "容许多高？不填默认100%", 'class': "form-control col-md-7 col-xs-12"}
                              ))
    space = fields.CharField(required=False, max_length=64, min_length=1, strip=True,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "容许最大上传kb", 'class': "form-control col-md-6 col-xs-6"}
                             ))
    other = fields.CharField(required=False, strip=True,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "扩展字段", 'class': "form-control col-md-7 col-xs-12"}
                             ))

    def clean(self):
        '''验证数据是否重复'''
        name = self.cleaned_data.get('name')
        ret = Domain.objects.filter(name=name).count()
        if self.status and ret:
            del self.cleaned_data['name']
        else:
            if ret:
                raise ValidationError('数据重复')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        try:
            self.status = int(kwargs.get('status', 0))
        except Exception as e:
            self.status = 0
        if kwargs.get('status'): del kwargs['status']
        super(LibraryForm, self).__init__(*args, **kwargs)
        self.fields['ptl_id'].widget.choices = PageTemplate.objects.all().values_list('id', 'name')
        self.fields['plugin_id'].widget.choices = Plugin.objects.all().values_list('id', 'name')

    class Meta:
        module = Library


class PageTemplateForm(Form):
    domain_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "模板名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    img = fields.ImageField(required=False,
                            widget=widgets.FileInput(attrs={'class': "form-control col-md-7 col-xs-12", }))

    def __init__(self, status=0, *args, **kwargs):
        self.status = status
        super(PageTemplateForm, self).__init__(*args, **kwargs)
        self.fields['domain_id'].widget.choices = Domain.objects.all().values_list('id', 'name')

    def clean(self):
        '''验证数据是否重复 1是修改 0是创建'''
        if self.status:
            if not self.cleaned_data.get('img'):
                del self.cleaned_data['img']
            return self.cleaned_data
        else:  # 创建数据
            if not self.cleaned_data.get('img'):
                raise ValidationError('图片不能为空')
        name = self.cleaned_data['name']
        domain_id = self.cleaned_data['domain_id']
        ret = PageTemplate.objects.filter(domain_id=domain_id, name=name).count()
        if ret:
            raise ValidationError('数据重复！')
        return self.cleaned_data

    class Meta:
        module = PageTemplate


class EmailGroupForm(Form):
    effect = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    name = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "组名称", 'class': "form-control col-md-7 col-xs-12"}
                            ))

    def __init__(self, status=0, *args, **kwargs):
        self.status = status
        super(EmailGroupForm, self).__init__(*args, **kwargs)
        self.fields['effect'].widget.choices = EmailGroup.effect_c


class EmailForm(Form):
    eg_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    user = fields.CharField(required=True, max_length=64, min_length=1, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "邮箱账户", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    passwd = fields.CharField(required=False, max_length=128,
                              widget=widgets.TextInput(
                                  attrs={'placeholder': "邮箱密码", 'class': "form-control col-md-7 col-xs-12", }
                              ))
    smtp = fields.CharField(required=False, max_length=128, strip=True,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "smtp.qq.com", 'class': "form-control col-md-7 col-xs-12"}
                            ))
    port = fields.IntegerField(required=False, max_value=65535, initial=25,
                               widget=widgets.TextInput(
                                   attrs={'placeholder': "端口", 'class': "form-control col-md-7 col-xs-12"}
                               ))
    auth = fields.CharField(required=False, widget=widgets.Select(attrs={'class': "form-control"}))
    issh = fields.CharField(required=False, widget=widgets.Select(attrs={'class': "form-control"}))

    def clean(self):
        eg_id = self.cleaned_data['eg_id']
        obj = EmailGroup.objects.filter(id=eg_id).first()
        if obj.effect == 1:
            ret = Email.objects.filter(eg=obj).count()
            if not self.status and ret:
                raise ValidationError('数据超过数量')
        return self.cleaned_data

    def __init__(self, status=0, *args, **kwargs):
        self.status = status
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['eg_id'].widget.choices = EmailGroup.objects.all().values_list('id', 'name')
        self.fields['auth'].widget.choices = Email.auth_c
        self.fields['issh'].widget.choices = Email.ssh_c


class TicketForm(Form):
    td_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    name = fields.CharField(required=True, max_length=128,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "票务名称", 'class': "form-control col-md-7 col-xs-12", }
                            ))
    code = fields.CharField(required=False, initial="6000{m}{d}{random|8}",
                            widget=widgets.TextInput(
                                attrs={'placeholder': "票务名称", 'class': "form-control col-md-7 col-xs-12", }
                            ))
    weight = fields.IntegerField(required=True, max_value=128, initial=1,
                                 widget=widgets.TextInput(
                                     attrs={'class': "form-control col-md-7 col-xs-12", }
                                 ))

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['td_id'].widget.choices = Domain.objects.all().values_list('id', 'name')

    class Meta:
        module = Ticket


class BillForm(Form):
    bd_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    phone = fields.CharField(required=True, max_length=11, min_length=11,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "手机号", 'class': "form-control col-md-7 col-xs-12", }
                             ))
    code = fields.CharField(required=True, max_length=128,
                            widget=widgets.TextInput(
                                attrs={'class': "hide", }
                            ))
    name = fields.CharField(required=True, max_length=32,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "姓名", 'class': "form-control col-md-7 col-xs-12", }
                            ))
    order_time = fields.CharField(required=False,
                                  widget=widgets.TextInput(
                                      attrs={'placeholder': "订单时间", 'class': "hide", }
                                  ))
    order_nub = fields.CharField(required=True,
                                 widget=widgets.TextInput(
                                     attrs={'placeholder': "订单号码", 'class': "hide", }
                                 ))
    bt_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    price = fields.FloatField(required=True,
                              widget=widgets.TextInput(
                                  attrs={'class': "form-control col-md-7 col-xs-12", }
                              ))
    channel = fields.CharField(required=True, max_length=128,
                               widget=widgets.TextInput(
                                   attrs={'placeholder': "渠道名称", 'class': "form-control col-md-7 col-xs-12", }
                               ))
    channel_code = fields.CharField(required=False, max_length=64,
                                    widget=widgets.TextInput(
                                        attrs={'placeholder': "渠道编码", 'class': "form-control col-md-7 col-xs-12", }
                                    ))
    sign_staus = fields.CharField(required=False, widget=widgets.Select(attrs={'class': "form-control"}))
    sign_time = fields.CharField(required=False,
                                 widget=widgets.TextInput(
                                     attrs={'placeholder': "签到时间", 'class': "form-control col-md-7 col-xs-12", }
                                 ))
    remarks = fields.CharField(required=False, max_length=128,
                               widget=widgets.TextInput(
                                   attrs={'placeholder': "备注", 'class': "form-control col-md-7 col-xs-12", }
                               ))

    def __init__(self, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        self.fields['sign_staus'].widget.choices = Bill.sign_staus_chioes
        self.fields['bt_id'].widget.choices = Ticket.objects.all().values_list('id', 'name')
        self.fields['bd_id'].widget.choices = Domain.objects.all().values_list('id', 'name')

    class Meta:
        module = Bill


class MemberForm(Form):
    phone = fields.CharField(required=True, max_length=11, min_length=11,
                             widget=widgets.TextInput(
                                 attrs={'placeholder': "手机号", 'class': "form-control col-md-7 col-xs-12", }
                             ))
    name = fields.CharField(required=False, max_length=32,
                            widget=widgets.TextInput(
                                attrs={'placeholder': "姓名", 'class': "form-control col-md-7 col-xs-12", }
                            ))
    sex = fields.CharField(required=False, widget=widgets.Select(attrs={'class': "form-control"}))
    age = fields.IntegerField(required=False,
                           widget=widgets.TextInput(
                               attrs={'placeholder': "年龄", 'class': "form-control col-md-7 col-xs-12", }
                           ))
    email = fields.EmailField(required=False,
                              widget=widgets.EmailInput(
                                  attrs={'placeholder': "邮箱", 'class': "form-control col-md-7 col-xs-12", }
                              ))
    company = fields.CharField(required=False, max_length=128,
                               widget=widgets.TextInput(
                                   attrs={'placeholder': "公司名称", 'class': "form-control col-md-7 col-xs-12", }
                               ))
    position = fields.CharField(required=False, max_length=64,
                                widget=widgets.TextInput(
                                    attrs={'placeholder': "职位", 'class': "form-control col-md-7 col-xs-12", }
                                ))
    def clean_sex(self):
        data = self.cleaned_data["sex"]
        try:
            data = int(data)
            if data > 1:
                raise ValidationError("性别格式不正确")
        except Exception as e:
            data = 1 if data == "男" else 0
        if data != 1 or data !=0:
            data = 1
        return data

    def clean_age(self):
        data = self.cleaned_data["age"]
        try:
            data = int(data)
            if data < 0:
                data = 0
        except Exception as e:
            data = 18
        return data

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['sex'].widget.choices = Memberinfo.sex_chiose

    class Meta:
        module = Memberinfo
