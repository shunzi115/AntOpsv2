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
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制厂商')
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
    update_date = models.DateTimeField(auto_now=True)


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
    other_ip = models.CharField(u'其他IP', max_length=255, null=True)
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
    update_date = models.DateTimeField(auto_now=True)

class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'内存插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(GB)')
    memo = models.TextField(u'备注', max_length=128, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)



class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插槽位',max_length=64)
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

# class UserProfile(AbstractBaseUser):
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    name = models.CharField(max_length=32)
    token = models.CharField(u'token', max_length=128, default=None, blank=True, null=True)
    department = models.CharField(u'部门', max_length=32, default=None, blank=True, null=True)
    # business_unit = models.ManyToManyField(BusinessUnit)
    tel = models.CharField(u'座机', max_length=32, default=None, blank=True, null=True)
    mobile = models.CharField(u'手机', max_length=32, default=None, blank=True, null=True)

    memo = models.TextField(u'备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, auto_now_add=True)
    # valid_begin = models.DateTimeField(blank=True, auto_now=True)
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField(blank=True, null=True)

    # groups = models.ManyToManyField



    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"

    def __unicode__(self):
        return self.name

    objects = UserManager()

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            #token=token,
            #department=department,
            #tel=tel,
            #memo=memo,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name ,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            name=name,
            #token=token,
            #department=department,
            #tel=tel,
            #memo=memo,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user