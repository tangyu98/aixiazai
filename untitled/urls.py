"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('reg', views.register),
    path('regis', views.register_ai),
    path('re_next', views.re_next),
    path('check_user', views.check_user),
    # path('log', views.login),
    url('^user/', include("user.urls")),
    url('^res/', include("resource.urls")),
    url('^bbs/', include("bbs.urls")),
    path('index', views.index),
    path('login1', views.login1, name="login1"),
    path('logout', views.logout, name="logout"),
    url('(?P<page>^\d*$)', views.index1, name="index1"),
    path('findpass', views.find_pass, name="find"),
    # path('celery', views.celery),
    path('<path:path>', views.path),
]
