from django.db import models


# 主域名
class Domain(models.Model):
    name = models.CharField('域名名称', max_length=64)
    url = models.URLField('域名地址', max_length=128)
    imgpath = models.CharField('服务器图片路径', max_length=128, default="/data_new/", null=True, blank=True)
    token = models.CharField('token', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '1-域名管理'
        unique_together = ('name', 'url')


# 域名下模板表
class PageTemplate(models.Model):
    domain = models.ForeignKey('Domain')
    name = models.CharField('模板名称', max_length=64)
    img = models.CharField('分析图', max_length=255)

    def __str__(self):
        return '%s-%s' % (self.domain, self.name)

    class Meta:
        verbose_name_plural = '2-模板类型'
        unique_together = ('domain', 'name')


# 程序插件表
class Plugin(models.Model):
    name = models.CharField('插件名称', max_length=64)
    table = models.CharField('表名称', max_length=64, unique=True)

    def __str__(self):
        return '%s-%s' % (self.name, self.table)

    class Meta:
        verbose_name_plural = '3-插件库'


# 程序库表
class Library(models.Model):
    ptl = models.ForeignKey('PageTemplate')
    plugin = models.ForeignKey('Plugin')
    weight = models.SmallIntegerField('权重', default=1)
    name = models.CharField('库名称', max_length=64)
    other =  models.CharField('备注信息', max_length=256)
    width = models.CharField('宽度', max_length=10, default='100%', null=True, blank=True)
    height = models.CharField('高度', max_length=10, default='100%', null=True, blank=True)
    space = models.IntegerField('空间', default=10000000, null=True, blank=True)


    def __str__(self):
        return '%s-%s' % (self.ptl, self.name)

    class Meta:
        verbose_name_plural = '3-模板库'


class Page(models.Model):
    pp = models.ForeignKey('PageTemplate')
    name = models.CharField('页面名称', max_length=64)
    url = models.CharField('链接', max_length=256)

    def __str__(self):
        return '%s-%s' % (self.pp, self.name)

    class Meta:
        verbose_name_plural = '4-用户页面管理'
        unique_together = ('pp', 'name')


class Imgs(models.Model):
    ip = models.ForeignKey('Page')
    il = models.ForeignKey('Library')
    title = models.CharField('标题', max_length=64, null=True)
    content = models.TextField('文本', null=True)
    url = models.CharField('链接', max_length=256, null=True, blank=True)
    img = models.CharField('图片', max_length=255)
    weight = models.SmallIntegerField('权重', default=1)
    ctime = models.CharField("创建时间", max_length=64, null=True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.il, self.title)

    class Meta:
        verbose_name_plural = '5-图片信息'
        unique_together = ('ip', 'il', 'title')


class Video(models.Model):
    vp = models.ForeignKey('Page')
    vl = models.ForeignKey('Library')
    name = models.CharField('标题', max_length=64)
    url = models.CharField('视频地址', max_length=128)
    weight = models.SmallIntegerField('权重', default=1)
    ctime = models.CharField("创建时间", max_length=64, null=True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.vl, self.name)

    class Meta:
        verbose_name_plural = '5-视频信息'


class Article(models.Model):
    ap = models.ForeignKey('Page')
    al = models.ForeignKey('Library')
    name = models.CharField('文章名称', max_length=64)
    author = models.CharField('作者', max_length=20, null=True, blank=True, default='admin')
    img = models.CharField('缩略图', max_length=256, null=True)
    amount = models.IntegerField('访问量', default=1, null=True, blank=True)
    summary = models.CharField('简介', max_length=255, null=True)
    content = models.TextField('文章内容')
    ctime = models.CharField("创建时间",max_length=64,null=True,blank=True)
    weight = models.SmallIntegerField('权重', default=1)

    def __str__(self):
        return '%s-%s' % (self.al, self.name)

    class Meta:
        verbose_name_plural = '5-文章信息'


class Personnel(models.Model):
    ppl = models.ForeignKey('Page')
    pl = models.ForeignKey('Library')
    name = models.CharField('姓名', max_length=64)
    ename = models.CharField('姓名拼音', max_length=128, null=True)
    company = models.CharField('公司名称', max_length=128, null=True)
    position = models.CharField('职位', max_length=128, null=True)
    pic = models.CharField('头像', max_length=256, null=True)
    summary = models.TextField('个人简介', null=True)
    stheme = models.CharField("演讲主题", max_length=255, null=True)
    sintroduce = models.TextField("演讲介绍", null=True)
    sdata = models.CharField("演讲日期", max_length=64, null=True)
    stime = models.CharField("演讲时间", max_length=64, null=True)
    meet = models.CharField("专场名称", max_length=128, null=True)
    meetaddr = models.CharField("会场地点", max_length=255, null=True)
    weight = models.SmallIntegerField('权重', default=1)
    ctime = models.CharField("创建时间",max_length=64,null=True,blank=True)

    def __str__(self):
        return '%s-%s' % (self.pl, self.name)

    class Meta:
        verbose_name_plural = '5-人员信息'


class Html(models.Model):
    hp = models.ForeignKey('Page')
    hl = models.ForeignKey('Library')
    name = models.CharField('名称', max_length=64)
    html = models.TextField('代码')
    weight = models.SmallIntegerField('权重', default=1)
    ctime = models.CharField("创建时间",max_length=64,null=True,blank=True)

    def __str__(self):
        return '%s-%s' % (self.hp, self.name)

    class Meta:
        verbose_name_plural = '6-自定义字段'


class Files(models.Model):
    fp = models.ForeignKey('Page')
    fl = models.ForeignKey('Library')
    user = models.ForeignKey('Personnel', null=True, blank=True)
    name = models.CharField('文件名', max_length=64)
    url = models.CharField('链接地址', max_length=255)
    weight = models.SmallIntegerField('权重', default=1)
    ctime = models.CharField("创建时间",max_length=64,null=True,blank=True)

    class Meta:
        unique_together = ('fp', 'fl', 'name')
        verbose_name = "文件下载管理"

    def __str__(self):
        return '%s-%s' % (self.fp, self.name)


class Contact(models.Model):
    name = models.CharField('姓名', max_length=32)
    email = models.EmailField('邮箱', unique=True)
    phone = models.CharField('手机', max_length=11, unique=True)
    company = models.CharField('公司', max_length=128, null=True)
    department = models.CharField('部门', max_length=64, null=True)
    position = models.CharField('职位', max_length=64, null=True)
    interest = models.CharField('兴趣', max_length=256, null=True)
    suggest = models.TextField('意见', null=True)
    creat_at = models.DateTimeField('创建时间', auto_now_add=True)
    weight = models.SmallIntegerField('权重', default=1)

    class Meta:
        verbose_name_plural = '6-加入我们信息'
        unique_together = ('name', 'phone')

    def __str__(self):
        return '%s-%s' % (self.name, self.phone)


class SysLog(models.Model):
    log_type_c = ((1, 'Info'), (2, 'Debug'), (3, 'WARN'), (4, 'ERROR'))
    user = models.CharField('操作用户', max_length=64)
    log_type = models.SmallIntegerField('日志类型', choices=log_type_c)
    content = models.TextField('日志内容')
    creat_time = models.DateTimeField(auto_now=True)


class EmailGroup(models.Model):
    effect_c = ((0, '接收'), (1, '发送'))
    name = models.CharField('组名称', max_length=64)
    effect = models.SmallIntegerField('作用', default=0, choices=effect_c)


class Email(models.Model):
    auth_c = ((0, '不认证'), (1, '认证'))
    ssh_c = ((0, '不加密'), (1, '加密'))

    eg = models.ForeignKey('EmailGroup')
    user = models.EmailField('邮件地址')
    passwd = models.CharField('密码', max_length=128, null=True)
    smtp = models.CharField('地址', max_length=128, null=True)
    port = models.IntegerField('端口', null=True)
    auth = models.SmallIntegerField('认证', choices=auth_c, null=True)
    issh = models.SmallIntegerField('加密', choices=ssh_c, null=True)


# 会员
class Memberinfo(models.Model):
    sex_chiose = ((1, "男"), (0, "女"))
    phone = models.CharField("手机号", max_length=11, unique=True)
    name = models.CharField("姓名", max_length=32, null=True, blank=True)
    sex = models.SmallIntegerField("性别",choices=sex_chiose,null=True, blank=True)
    age = models.SmallIntegerField("年龄", null=True, blank=True)
    email = models.EmailField("邮箱", null=True, blank=True)
    company = models.CharField("公司", max_length=256, null=True, blank=True)
    position = models.CharField("职位", max_length=256, null=True, blank=True)
    ctime = models.CharField("创建时间",max_length=64,null=True,blank=True)

    class Meta:
        verbose_name = "会员管理"

    def __str__(self):
        return '%s-%s' % (self.name, self.phone)


# 订单信息
class Bill(models.Model):
    sign_staus_chioes = ((0,"未签到"),(1,"已签到"))
    bd = models.ForeignKey("Domain")
    phone = models.CharField("手机号", max_length=11)
    code = models.CharField("签到码", max_length=64,null=True,blank=True)
    name = models.CharField("姓名", max_length=32, null=True, blank=True)
    order_time = models.CharField("订单时间", max_length=64,null=True,blank=True)
    order_nub = models.CharField("订单号", max_length=64,null=True,blank=True)
    bt = models.ForeignKey("Ticket")
    price = models.FloatField("门票价格",)
    channel = models.CharField("渠道",max_length=64,null=True,blank=True)
    channel_code = models.CharField("渠道编码",max_length=64,null=True,blank=True)
    sign_staus = models.SmallIntegerField("签到状态",choices=sign_staus_chioes,default=0)
    sign_time = models.CharField("签到时间",max_length=64,null=True,blank=True)
    remarks = models.CharField("备注",max_length=256,null=True,blank=True)
    ctime = models.CharField("创建时间",max_length=256,null=True,blank=True)

    class Meta:
        verbose_name = "订单信息"
        unique_together = ("order_nub","code","phone")

    def __str__(self):
        return '%s-%s' % (self.phone, self.order_nub)


# 我的收藏
class MemberPCollect(models.Model):
    mpc = models.ForeignKey("Memberinfo", verbose_name="用户")
    mp = models.ForeignKey("Personnel", verbose_name="嘉宾")

    class Meta:
        verbose_name = "会员收藏"
        unique_together = ("mpc","mp")

    def __str__(self):
        return '%s-%s' % (self.mpc, self.mp)


# 文档收藏
class FileCollect(models.Model):
    mf = models.ForeignKey("Memberinfo", verbose_name="用户")
    mp = models.ForeignKey("Files", verbose_name="文档")

    class Meta:
        verbose_name = "文档收藏"
        unique_together = ("mf","mp")

    def __str__(self):
        return '%s-%s' % (self.mf, self.mp)


# 票务
class Ticket(models.Model):
    td = models.ForeignKey("Domain")
    name = models.CharField("票务名称", max_length=11)
    code = models.CharField("编码规则",max_length=64,null=True)
    weight = models.SmallIntegerField('权重', default=1)

    class Meta:
        verbose_name = "票务管理"

    def __str__(self):
        return self.name


# 议题
class Meetissue(models.Model):
    dm = models.ForeignKey("Domain")
    name = models.CharField("姓名", max_length=32)
    company = models.CharField("公司", max_length=128)
    position = models.CharField("职位", max_length=64)
    phone = models.CharField("手机号", max_length=11)
    email = models.EmailField("邮箱", max_length=256)
    addr = models.CharField('地址', max_length=256)
    photo = models.TextField('照片')
    summary = models.CharField('个人简介', max_length=256)
    speech_experience = models.TextField('演讲经验',null=True,blank=True)
    interest = models.CharField('兴趣专场', max_length=256)
    remark = models.CharField('备注', max_length=256,null=True,blank=True)
    theme = models.CharField('演讲主题', max_length=256)
    content = models.TextField('演讲内容')
    innovate = models.SmallIntegerField('主题创新')
    hot_topic = models.SmallIntegerField('话题热度')
    experience = models.SmallIntegerField('实战经验')
    generality = models.SmallIntegerField('通用性')
    suggest = models.TextField('意见建议',null=True,blank=True)
    referee = models.CharField("推荐人", max_length=32, null=True)
    ctime = models.DateTimeField("创建时间", auto_now=True)

    class Meta:
        verbose_name = "议题提交"

    def __str__(self):
        return '%s-%s' % (self.name, self.theme)


# 赞助意向
class Sponsor(models.Model):
    ds = models.ForeignKey("Domain")
    name = models.CharField("姓名", max_length=32)
    company = models.CharField("公司", max_length=128)
    phone = models.CharField("手机号", max_length=11)
    position = models.CharField("职位", max_length=64)
    email = models.EmailField("邮箱", max_length=256)
    intention = models.TextField("赞助意向")
    ctime = models.DateTimeField("创建时间", auto_now=True)

    class Meta:
        verbose_name = "赞助意向"

    def __str__(self):
        return '%s-%s' % (self.name, self.intention)
