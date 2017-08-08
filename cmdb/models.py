#!/usr/bin/evn python
# -*- coding:utf-8 -*-

from django.db import models







class Idc(models.Model):
    name = models.CharField(u'机房名称', max_length=32, unique=True)
    address = models.CharField(u'机房地址', max_length=128)
    contact = models.CharField(u'联系人', max_length=32, null=True)
    telephone = models.CharField(u'机房电话', max_length=32, null=True)
    contact_phone = models.CharField(u'移动电话', max_length=32, null=True)
    cabinet = models.CharField(u'机柜信息', max_length=64, null=True)
    ip_range = models.CharField(u'IP范围', max_length=64, null=True)
    bandwidth = models.CharField(u'接入带宽', max_length=24, null=True)

class Nic(models.Model):
    name = models.CharField(u'网卡名', max_length=26)


