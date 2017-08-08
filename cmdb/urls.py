#!/usr/bin/env python
# -*- coding: -*-

from django.conf.urls import url
from cmdb import views

urlpatterns = [
    url(r'^assest/', views.index, name="assest"),
]