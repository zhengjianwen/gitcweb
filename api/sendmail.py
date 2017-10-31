#!/usr/bin/env python
# -*- coding=utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from bmpdata.models import Email
from django.core.mail import send_mail
from django.shortcuts import render, redirect,HttpResponse
from smtplib import SMTP_SSL,SMTP
from email.header import Header
from email.mime.text import MIMEText
import smtplib


def syssendmail(request):
    try:
        send_mail('麒麟会欢迎你2017',
                  '欢迎注册麒麟会网址',
                  'member@kylinclub.org',
                    ['574601624@qq.com',], fail_silently=True)
        return HttpResponse('发送成功')
    except Exception as e:
        return HttpResponse('%s'%(e))





class SendMail:

    def __init__(self,sendobj,recv_mail_list,sendname, toname, title, content):
        self.mail_host = sendobj.smtp  # 设置服务器
        self.mail_user = sendobj.user  # 用户名
        self.mail_pass = sendobj.passwd  # 口令
        self.mail_port = sendobj.port      # 端口
        self.mail_ssh = True if sendobj.issh else False     # 是否是加密端口
        self.content = content # 邮件内容
        self.sendname = sendname
        self.toname = toname
        self.title = title # 邮件标题
        self.encoding = "utf-8" # 邮件编码格式
        self.sender = sendobj.user #发件地址
        self.receivers = recv_mail_list # 收件箱

    def start(self):
        self.msg()
        if self.mail_ssh:
            self.ssh()
        else:
            self.pt()

    def msg(self):
        self.msg = MIMEText(self.content, "plain", self.encoding)
        self.msg["Subject"] = Header(self.title, self.encoding)
        self.msg["from"] = self.mail_user
        self.msg["to"] = self.toname

    def ssh(self):
        smtp = SMTP_SSL(self.mail_host)
        smtp.set_debuglevel(0)
        smtp.ehlo(self.mail_user)
        smtp.login(self.mail_user,self.mail_pass)
        smtp.sendmail(self.mail_user, self.receivers, self.msg.as_string())
        smtp.quit()

    def pt(self):
        server = smtplib.SMTP(self.mail_host, self.mail_port)
        server.set_debuglevel(1)
        server.login(self.mail_user, self.mail_pass)
        server.sendmail(self.mail_user, self.receivers, self.msg.as_string())
        server.quit()

if __name__ == '__main__':
    obj = SendMail(1,'海瑞网络','海瑞','密码找回','内容：这个海瑞网络发送的测试邮件',)
    obj.start()