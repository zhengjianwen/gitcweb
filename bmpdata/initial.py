from bmpdata.models import EmailGroup, Plugin

PLUGIN = [{'name':'图文插件','table':'Imgs'},
          {'name':'文章插件','table':'Article'},
          {'name':'人员插件','table':'Personnel'},
          {'name':'视频插件','table':'Video'},
          {'name':'自定义插件','table':'Html'},
          {'name':'文件插件','table':'Files'},
          ]

EMAILGROUP = [{'name':'默认发件人'},
              {'name':'加入我们收件组'}
              ]

Email = [

]

def InitialData():
    plagin_count = Plugin.objects.all().count()
    if plagin_count == 0:
        for val in PLUGIN:
            try:
                Plugin.objects.create(**val)
            except Exception as e:
                continue
    eg_count = EmailGroup.objects.all().count()
    if eg_count == 0:
        for val in EMAILGROUP:
            try:
                EmailGroup.objects.create(**val)
            except Exception as e:
                continue