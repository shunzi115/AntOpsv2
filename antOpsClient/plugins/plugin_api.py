#!/usr/bin/env python
# -*- coding:utf-8 -*-

def LinuxSysInfo():
    '''
    call Linux  collect model
    :return: Linux info data
    '''
    from plugins.Linux import sysinfo
    return sysinfo.collect()


def WindowsSysInfo():
    # from plugins.Window import sysinfo as win_sysinfo
    # return win_sysinfo.collect()
    pass