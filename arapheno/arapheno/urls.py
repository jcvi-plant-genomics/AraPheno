"""arapheno URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin

import home.views
import phenotypedb.views


urlpatterns = [
    url(r'^$',home.views.home),
    url(r'phenotypes/$',phenotypedb.views.PhenotypeList.as_view(),name="phenotypes"),
    url(r'phenotype/(?P<pk>[0-9]+)/$',phenotypedb.views.PhenotypeDetail.as_view(),name="phenotype_detail"),
    url(r'studies/$',phenotypedb.views.StudyList.as_view(),name="studies"),
    url(r'study/(?P<pk>[0-9]+)$',phenotypedb.views.StudyDetail.as_view(),name="study_detail"),
    url(r'about/$',home.views.about),
]
