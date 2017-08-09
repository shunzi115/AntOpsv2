#!/usr/bin/evn python
# -*- coding:utf-8 -*-


from django.db import models

class Asset(models.Model):
    asset_type_choices = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),

    )
    name = models.CharField(u'名称', max_length=64, unique=True)
    management_ip = models.GenericIPAddressField(u'管理IP')
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    manufactory = models.CharField(u'制厂商', max_length=64, null=True)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True)
    status_choices = (
        (0, '在线'),
        (1, '已下线'),
        (2, '备用'),
        (3, '故障'),
        (4, '未知')
    )
    status_type = models.SmallIntegerField(choices=status_choices, default=0)
    memo = models.TextField(u'备注', null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)

class IDC(models.Model):
    name = models.CharField(u'机房名称', max_length=32, unique=True)
    address = models.CharField(u'机房地址', max_length=128)
    contact = models.CharField(u'联系人', max_length=32, null=True)
    telephone = models.CharField(u'机房电话', max_length=32, null=True)
    contact_phone = models.CharField(u'移动电话', max_length=32, null=True)
    cabinet = models.CharField(u'机柜信息', max_length=64, null=True)
    ip_range = models.CharField(u'IP范围', max_length=64, null=True)
    bandwidth = models.CharField(u'接入带宽', max_length=24, null=True)

class Server(models.Model):
    asset = models.OneToOneField('Asset')
    server_type_choices = (
        (0, '物理机'),
        (1, '虚拟机'),
    )
    server_type = models.SmallIntegerField(choices=server_type_choices, verbose_name="服务器类型",default=0)
    # other_ip = models.CharField(u'其他IP', max_length=255, null=True)
    model = models.CharField(u'型号', max_length=128, null=True)
    os_type = models.CharField(u'操作系统类型', max_length=64)
    os_release = models.CharField(u'操作系统版本', max_length=64)

class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    network_type_choices = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '防火墙'),
    )
    network_type = models.SmallIntegerField(choices=network_type_choices, verbose_name="网络设备类型", default=0)
    vlan_ip = models.GenericIPAddressField(u'VlanIP', null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP', null=True)
    model = models.CharField(u'型号', max_length=128, null=True)
    prot_num = models.SmallIntegerField(u'端口数', null=True)
    device_detail = models.TextField(u'设置详细配置', null=True)

class CPU(models.Model):
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号', max_length=128)
    cpu_count = models.SmallIntegerField(u'物理CPU个数')
    cpu_core_count = models.SmallIntegerField(u'CPU核数')
    memo = models.TextField(u'备注', null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)

class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'内存插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(GB)')
    memo = models.TextField(u'备注', max_length=128, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)

class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, null=True)
    slot = models.CharField(u'插槽', max_length=64)
    model = models.CharField(u'硬盘型号', max_length=128, null=True)
    capacity = models.FloatField(u'磁盘容量')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSC', 'SSD'),
    )
    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)

class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64)
    sn = models.CharField(u'SN号', max_length=128, null=True)
    model = models.CharField(u'网卡型号', max_length=128, null=True)
    macaddress = models.CharField(u'MAC地址', max_length=128, null=True)
    ipaddress = models.GenericIPAddressField(u'IP', null=True)
    netmask = models.CharField(u'子网掩码', max_length=64, null=True)
    bonding = models.CharField(u'绑定网卡', max_length=64, null=True)
    memo = models.TextField(u'备注', max_length=128, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)

class RaidAdaptor(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, null=True)
    slot = models.CharField(u'插口', max_length=64)
    model = models.CharField(u'型号', max_length=64, null=True)
    memo = models.TextField(u'备注', unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)
