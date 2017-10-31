from bmpdata.models import SysLog


def write_log(user,log_type,content):
    info = {
        'user':user,
        'log_type':log_type,
        'content':content,
    }
    try:
        SysLog.objects.create(**info)
    except Exception as e:
        SysLog.objects.create('system',4,'系统日志写入失败，原因为：%s' % e)