import hashlib
import uuid,xlwt,os,shutil,time
from webserver.settings import STATIC_ROOT,BASE_DIR

def md5(data=None):
    if not data:
        data = str(uuid.uuid1()).encode('utf-8')
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


class Export_data:

    def __init__(self,data,keys,title):
        self.basedata = list(data) # 用户传来得数据
        self.keys = keys  # 获取key
        self.title = title # excel标题 ["验票码"]  与key的索引相对应
        self.data = self._makedata() # 最终需要写入的数据列表

    def _makedata(self):
        data = [self.title,]
        for dic in self.basedata:
            tmp = []
            for t in self.keys:
                tmp.append(dic[t])
            data.append(tmp)

        return data

    def down_url(self):
        filename = self._write_to_excel()
        if filename:
            return "/static/down/xls/%s"%filename
        return None

    def _write_to_excel(self):
        if not self.data:
            return None
        excel = xlwt.Workbook(encoding="utf-8")
        sheet = excel.add_sheet('database', cell_overwrite_ok=True)
        # write data
        for x, row in enumerate(self.data):
            for y, val in enumerate(row):
                sheet.write(x, y, val)
        # save data to
        today = time.time()
        file_name = str(int(today))
        file_name = file_name + ".xls"
        excel.save(file_name)
        # 移动文件 /static/tmp/file_name.xls
        old_path = os.path.join(BASE_DIR, file_name)
        new_file_path = os.path.join(STATIC_ROOT, 'down', 'xls', file_name)
        if os.path.exists(old_path):
            shutil.move(old_path, new_file_path)
            return file_name
        return
