"""main URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^results/files/([0-9]{4})/([0-9]{2})/([0-9]){2}/(.*SC2Replay){1}$', views.results, name = 'results'),
    url(r'^test/$', views.test, name = 'test'),

    # url(r'^results/.*SC2Replay', views.results, name = 'results'),
]
