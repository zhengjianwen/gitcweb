import hashlib,time,uuid,os,requests,json,xlrd
from gitc.models import Personnel
from pypinyin import lazy_pinyin
from webserver.settings import BASE_DIR, UPPORT, UPURL, UPKEY


class ImgUp:
    def __init__(self, img, pathname):
        self.img = img
        self._key = UPKEY
        self._pathname = pathname
        self._url = UPURL % UPPORT

    def start(self):
        path = self._recv()
        if path:
            p = self._up(path[0], path[1])
            return p

    def _up(self, path, filename):
        with open(path, 'rb') as f:
            data = f.read()
        if data:
            os.remove(path)
        cookies = {'gitc': 'www.kylinclub.com'}
        files = {'file': (filename, data)}
        rdata = requests.post(self._url, files=files, cookies=cookies, data={'token': self._verify(), 't': self.t})
        dic = json.loads(rdata.text)
        if dic.get('status'):
            return dic.get('data')

    def _verify(self):
        self.t = time.time()
        m = hashlib.md5()
        data = '%s-%s' % (self.t, self._key)
        m.update(data.encode('utf-8'))
        return m.hexdigest()

    def _recv(self):
        if self.img:
            filename = str(uuid.uuid1()) + self.img.name
            img_path = os.path.join(BASE_DIR, '../../status', self._pathname, filename)
            with open(img_path, 'wb') as f:
                for data in self.img.chunks():
                    f.write(data)
            return img_path, filename


class UploadFile:
    '''
    文件上传功能，支持xls,xlsx 格式的excel.必须使用模板提交。

    '''

    def __init__(self, fileobj):
        self.file = fileobj

    def get_data(self):
        path = self._wirte_excel()
        if path:
            data = self._read_data(path)
            return data

    def _wirte_excel(self):
        '''
        写入excel文件
        :param request:
        :return: file path
        '''
        if '.xls' not in self.file.name[-5:]:
            return False
        filename = 'aaaa%s' % self.file.name
        file_path = os.path.join(BASE_DIR, '../../status', 'down', 'xls', filename)
        with open(file_path, 'wb') as f:
            for i in self.file.chunks():
                f.write(i)
        return file_path

    def _read_data(self, path):
        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        title = ['cid', 'cname', 'ename', 'company', 'position', 'summary']
        data = []
        for i in range(nrows):
            # 获取每行数据
            row_val = table.row_values(i)
            if i == 0:
                continue
            tmp = {'status': False, 'data': {}}
            # 将值变成键值对的方式保存
            for index, key in enumerate(title):
                if key == 'ename':
                    val = ''.join(lazy_pinyin(tmp['data'].get('cname')))
                else:
                    val = row_val[index]
                tmp['data'][key] = val
            # 数据验证
            if self._data_review(tmp['data']):
                tmp['status'] = True
            else:
                tmp['status'] = False
            data.append(tmp)

        return data

    def _data_review(self, data):
        '''
        数据验证
        :param data:
        :return:
        '''
        cname = data.get('cname')
        ename = data.get('ename')
        ret = Person.objects.filter(cname=cname, ename=ename).count()
        if ret:
            return False
        return True
