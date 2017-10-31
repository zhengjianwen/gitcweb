# HairuiBPM
web api 后台管理系统
海瑞博客 http://www.hairuinet.com

开发语言：python + Bootstrap3 + js + ajax
开发框架：django 1.10.1

适用于网站资源系统的管理，前后端分离管理。

功能说明

自定义插件模板
  文章插件
  图片插件
  人员插件 - 支持批量导入
  视频插件
  html代码插件
  
自定义页面模板
  根据建立的域名，可以在域名下添加对应的模板关联
  页面模板 生成 多个页面的api 
  可以对每个插件内容添加数据。
  
用户认证
  django 自带认证。
  默认账户：admin  密码：123456
  
  
  程序安装：
  
  将数据库删除
  1.清空status/tmp 下图片
  2. python manage.py makemigrations
  3. python manage.py migrate
  4.创建超级管理员 python manage.py createsuperuser
  
  5.启动程序
  python manage.py runserver 0.0.0.0:80
  
  后台登录
  http://127.0.0.1/gitcadmin/login.html
  输入账户和密码。
  
  第一步
  创建网站，
  第二步
  创建网站页面
  第三步
  为页面添加插件
  模板创建完成
  
  
