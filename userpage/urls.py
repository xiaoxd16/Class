"""class URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include,url
from django.contrib import admin
from .views import *
urlpatterns = [
	url(r'^bind?$',PersonBind.as_view()),
	url(r'^class/all?$',AllClass.as_view()),
	url(r'^class/my?$',MyClass.as_view()),
	url(r'^class/info?$',ClassInfo.as_view()),
	url(r'^info?$',PersonInfo.as_view()),
	url(r'^class/create?$',CreateClass.as_view()),
	url(r'^class/exit?$',ExitClass.as_view()),
	url(r'^class/insert?$',InsertClass.as_view()),
]
