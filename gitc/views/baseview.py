#!/usr/bin/env python     
# -*- coding:utf-8 -*-
#  Author   Hairui
from django.views import View
from bmpdata.models import Personnel, SysLog
from pypinyin import lazy_pinyin
from webserver.settings import BASE_DIR, UPKEY, UPURL, UPPORT, IMG_STATUS
import uuid, os, requests, time, hashlib, json, xlrd


class BaseView(View):
    def upimg(self, imgobj, domain, path_name="images", *args, **kwargs):
        url = ''
        status = True
        library_obj = kwargs.get("library",None)
        if library_obj:
            status = self._size(imgobj,library_obj)
        if status and self._path(domain, path_name):
            filename = self._recv(imgobj, domain, path_name)
            url = "%s/static/%s/%s" % (domain.url, path_name, filename)
        return url

    def _size(self, img, library):
        try:
            xzsize = int(library.space)
            size = int(img.size)
            if size <= xzsize:
                status = True
            else:
                status = False
        except Exception as e:
            status = True
        return status

    def _recv(self, img, domain, path_name):
        _, hz = str(img.name).rsplit('.', 1)
        filename = '%s.%s' % (str(uuid.uuid1()), hz)
        base_path = domain.imgpath
        img_path = os.path.join(base_path, path_name, filename)
        with open(img_path, 'wb') as f:
            for data in img.chunks():
                f.write(data)
        return filename

    def _path(self, domain, path_name):
        try:
            base_path = domain.imgpath
            img_path = os.path.join(base_path, path_name)
            if not os.path.isdir(img_path):
                os.makedirs(img_path)
            return True
        except Exception as e:
            return False

    def _up(self, path, filename):
        '''上传文件'''
        with open(path, 'rb') as f:
            data = f.read()
        if data:
            os.remove(path)
        _url = UPURL % UPPORT
        cookies = {'gitc': 'www.kylinclub.com'}
        files = {'file': (filename, data)}
        rdata = requests.post(_url, files=files, cookies=cookies, data={'token': self._verify(), 't': self.t})
        dic = json.loads(rdata.text)
        if dic.get('status'):
            return dic.get('path')

    def _verify(self):
        self.t = time.time()
        m = hashlib.md5()
        data = '%s-%s' % (self.t, UPKEY)
        m.update(data.encode('utf-8'))
        return m.hexdigest()

    def excel_to_dict(self, file):
        if not file:
            return
        file_path = os.path.join(BASE_DIR, file.name)
        with open(file_path, 'wb') as f:
            for data in file.chunks():
                f.write(data)
        data = self._read_data(file_path)
        return data

    def _read_data(self, path):
        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        title = ['cid', 'name', 'ename', 'company', 'position', 'summary', 'stheme', 'sintroduce', 'sdata', 'stime',
                 'meet', 'meetaddr']
        data = []
        for i in range(nrows):
            # 获取每行数据
            row_val = table.row_values(i)
            print(row_val)
            if i == 0:
                continue
            tmp = {'status': False, 'data': {}}
            # 将值变成键值对的方式保存
            for index, key in enumerate(title):
                if key == 'ename':
                    val = ''.join(lazy_pinyin(tmp['data'].get('name')))
                else:
                    val = row_val[index]
                tmp['data'][key] = val
            # 数据验证
            if self._data_review(tmp['data']):
                tmp['status'] = True
            else:
                tmp['status'] = False
            data.append(tmp)
        os.remove(path)
        return data

    def _data_review(self, data):
        '''
        数据验证
        :param data:
        :return:
        '''
        cname = data.get('name')
        ename = data.get('ename')
        ret = Personnel.objects.filter(name=cname, ename=ename).count()
        return True if ret else True

    def write_log(self, user, log_type, content):
        info = {
            'user': user,
            'log_type': log_type,
            'content': content,
        }
        try:
            SysLog.objects.create(**info)
        except Exception as e:
            SysLog.objects.create('system', 4, '系统日志写入失败，原因为：%s' % e)
