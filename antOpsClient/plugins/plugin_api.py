#!/usr/bin/env python
# -*- coding:utf-8 -*-

def LinuxSysInfo():
    '''
    call linux  collect model
    :return: linux info data
    '''
    from plugins.linux import sysinfo
    return sysinfo.collect()

def WindowsSysInfo():
    # from plugins.Window import sysinfo as win_sysinfo
    # return win_sysinfo.collect()
    pass