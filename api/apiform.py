from bmpdata.models import Contact,Meetissue,Sponsor,Domain
from django.forms.forms import Form
from django.forms import fields, widgets
from django.core.exceptions import ValidationError
import re


class ContactForm(Form):
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    email = fields.EmailField(required=True,max_length=64, min_length=6, strip=True,)
    phone = fields.CharField(required=True,max_length=11)
    company = fields.CharField(required=True,max_length=128, min_length=1,)
    department = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    position = fields.CharField(required=True,max_length=64, min_length=1, strip=True)
    interest = fields.CharField(required=False,max_length=64, min_length=1, strip=True)
    suggest = fields.CharField(required=False,max_length=64, min_length=1, strip=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            data = ['133','131','130','158','159','139','138','136','135','189','180','170','177','175','153','173','181']
            int(phone)
            if phone[:3] in data:
               return phone
            else:
                raise ValidationError('手机号不正确')
        except Exception as e:
            raise ValidationError(e)

    def clean_interest(self):
        val = self.cleaned_data.get('interest')
        if val:
            return ''.join(val)
        return val

    class Meta:
        module = Contact


class SponsorForm(Form):
    ds_id = fields.CharField(required=True, widget=widgets.Select(attrs={'class': "form-control"}))
    name = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    company = fields.CharField(required=True,max_length=128, min_length=1, strip=True,)
    phone = fields.CharField(required=True,max_length=11,strip=True)
    position = fields.CharField(required=True,strip=True)
    email = fields.EmailField(required=True, strip=True,)
    intention = fields.CharField(required=False)

    def clean_phone(self):
        phone = str(self.cleaned_data['phone']).strip()
        nub = Sponsor.objects.filter(phone=phone).count()
        if nub > 5:
            raise ValidationError('手机号提交过多！')
        if len(re.findall(r"1\d{10}",phone)) == 0 :
            raise ValidationError("手机号不正确！")
        return phone

    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)
        self.fields['ds_id'].widget.choices = Domain.objects.all().values_list('id', 'name')

    class Meta:
        module = Sponsor


class MeetissueForm(Form):
    dm_id = fields.CharField(required=True, widget=widgets.Select())
    name = fields.CharField(required=True,max_length=32, min_length=1, strip=True,)
    company = fields.CharField(required=True,max_length=128, min_length=1, strip=True,)
    position = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    phone =fields.CharField(required=True)
    email = fields.EmailField(required=True,max_length=255, min_length=5, strip=True,)
    addr = fields.CharField(required=True,max_length=255, strip=True,)
    photo = fields.CharField(required=True)
    summary = fields.CharField(required=True,max_length=256, strip=True,)
    speech_experience = fields.CharField(required=False,)
    interest = fields.CharField(required=True,max_length=64, min_length=1, strip=True,)
    remark = fields.CharField(required=False,max_length=256, strip=True,)
    theme = fields.CharField(required=True,max_length=256, min_length=1, strip=True,)
    content = fields.CharField(required=True,)
    referee = fields.CharField(required=False,max_length=32)
    innovate = fields.IntegerField(required=True)
    hot_topic = fields.IntegerField(required=True)
    experience = fields.IntegerField(required=True)
    generality = fields.IntegerField(required=True)
    suggest = fields.CharField(required=False,)

    class Meta:
        module = Meetissue

    def __init__(self, *args, **kwargs):
        super(MeetissueForm, self).__init__(*args, **kwargs)
        self.fields['dm_id'].widget.choices = Domain.objects.all().values_list('id', 'name')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        nub = Sponsor.objects.filter(phone=phone).count()
        if nub > 2:
            raise ValidationError('手机号提交过多！')
        if not re.findall(r"1[3578]{1}\d{9}",phone):
            raise ValidationError("手机号不正确！")
        return phone