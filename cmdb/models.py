#!/usr/bin/evn python
# -*- coding:utf-8 -*-


# cmdb models include
# server nic
# server assest
# server ram
# server drive
# server cpu
# NetworkDevice
# idc
#
#


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
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制厂商')
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True)
    idc = models.ForeignKey('Idc', verbose_name=u'IDC机房', null=True)
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
    update_date = models.DateTimeField(auto_now=True)


class Idc(models.Model):
    name = models.CharField(u'机房名称', max_length=32, unique=True)
    address = models.CharField(u'机房地址', max_length=128)
    contact = models.CharField(u'联系人', max_length=32, null=True)
    telephone = models.CharField(u'机房电话', max_length=32, null=True)
    contact_phone = models.CharField(u'移动电话', max_length=32, null=True)
    cabinet = models.CharField(u'机柜信息', max_length=64, null=True)
    ip_range = models.CharField(u'IP范围', max_length=64, null=True)
    bandwidth = models.CharField(u'接入带宽', max_length=24, null=True)

class CPU(models.Model):
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"

    def __str__(self):
        return self.cpu_model


class Nic(models.Model):
    name = models.CharField(u'网卡名', max_length=26)








class Server(models.Model):
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0,'PC服务器'),
        (1,'刀片机'),
        (2,'小型机'),
    )
    created_by_choices = (
        ('auto','Auto'),
        ('manual','Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices,verbose_name="服务器类型",default=0)
    created_by = models.CharField(choices=created_by_choices,max_length=32,default='auto') #auto: auto created,   manual:created manually
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True,null=True) #for vitural server
    #sn = models.CharField(u'SN号',max_length=128)
    #management_ip = models.CharField(u'管理IP',max_length=64,blank=True,null=True)
    #manufactory = models.ForeignKey(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(verbose_name=u'型号',max_length=128,null=True, blank=True )
    # 若有多个CPU，型号应该都是一致的，故没做ForeignKey

    #nic = models.ManyToManyField('NIC', verbose_name=u'网卡列表')
    #disk
    raid_type = models.CharField(u'raid类型',max_length=512, blank=True,null=True)
    #physical_disk_driver = models.ManyToManyField('Disk', verbose_name=u'硬盘',blank=True,null=True)
    #raid_adaptor = models.ManyToManyField('RaidAdaptor', verbose_name=u'Raid卡',blank=True,null=True)
    #memory
    #ram_capacity = models.IntegerField(u'内存总大小GB',blank=True)
    #ram = models.ManyToManyField('Memory', verbose_name=u'内存配置',blank=True,null=True)

    os_type  = models.CharField(u'操作系统类型',max_length=64, blank=True,null=True)
    os_distribution =models.CharField(u'发型版本',max_length=64, blank=True,null=True)
    os_release  = models.CharField(u'操作系统版本',max_length=64, blank=True,null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
        #together = ["sn", "asset"]

    def __str__(self):
        return '%s sn:%s' %(self.asset.name,self.asset.sn)


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0,'路由器'),
        (1,'交换机'),
        (2,'负载均衡'),
        (4,'VPN设备'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices,verbose_name="服务器类型",default=0)

    vlan_ip = models.GenericIPAddressField(u'VlanIP',blank=True,null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP',blank=True,null=True)
    #sn = models.CharField(u'SN号',max_length=128,unique=True)
    #manufactory = models.CharField(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(u'型号',max_length=128,null=True, blank=True )
    firmware = models.ForeignKey('Software',blank=True,null=True)
    port_num = models.SmallIntegerField(u'端口个数',null=True, blank=True )
    device_detail = models.TextField(u'设置详细配置',null=True, blank=True )

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model =  models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return '%s:%s:%s' % (self.asset_id,self.slot,self.capacity)
    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")
    auto_create_fields = ['sn','slot','model','capacity']

class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插槽位',max_length=64)
    #manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128,blank=True,null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64,choices=disk_iface_choice,default='SAS')
    memo = models.TextField(u'备注', blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    auto_create_fields = ['sn','slot','manufactory','model','capacity','iface_type']
    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id,self.slot,self.capacity)


class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64, blank=True,null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model =  models.CharField(u'网卡型号', max_length=128, blank=True,null=True)
    macaddress = models.CharField(u'MAC', max_length=64,unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True,null=True)
    netmask = models.CharField(max_length=64,blank=True,null=True)
    bonding = models.CharField(max_length=64,blank=True,null=True)
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id,self.macaddress)
    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"
        #unique_together = ("asset_id", "slot")
        unique_together = ("asset", "macaddress")
    auto_create_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding']

class RaidAdaptor(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插口',max_length=64)
    model = models.CharField(u'型号', max_length=64,blank=True,null=True)
    memo = models.TextField(u'备注', blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ("asset", "slot")

class Manufactory(models.Model):
    manufactory = models.CharField(u'厂商名称',max_length=64, unique=True)
    support_num = models.CharField(u'支持电话',max_length=30,blank=True)
    memo = models.CharField(u'备注',max_length=128,blank=True)
    def __str__(self):
        return self.manufactory
    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    parent_unit = models.ForeignKey('self',related_name='parent_level',blank=True,null=True)
    name = models.CharField(u'业务线',max_length=64, unique=True)

    #contact = models.ForeignKey('UserProfile',default=None)
    memo = models.CharField(u'备注',max_length=64, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

class Tag(models.Model):
    name = models.CharField('Tag name',max_length=32,unique=True )
    creater = models.ForeignKey('UserProfile')
    create_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name


