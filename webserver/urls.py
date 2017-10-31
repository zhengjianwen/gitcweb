"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.shortcuts import redirect
from webserver import settings
from webserver.views import page_not_found,permission_denied,page_error

def error(request):
    return redirect('http://www.thegitc.com')

def favicon(request):
    return redirect("/static/img/logo.png")


#handler403 = permission_denied
#handler404 = page_not_found
#handler500 = page_error

urlpatterns = [
    # url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve'),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^kingadmin/', admin.site.urls),
    url(r'^favicon.ico', favicon),
    url(r'^gitcadmin/', include('gitc.urls')),
    url(r'^api/', include('api.urls')),
    url(r'', error),
]


