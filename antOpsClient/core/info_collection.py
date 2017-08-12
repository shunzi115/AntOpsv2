#!/usr/bin/env python
# -*- coding:utf-8 -*-

## this system only collect linux  system info.
## about windows system info, next release will add it.

import platform,sys, json
from plugins import plugin_api

class InfoCollection(object):
    def __init__(self):
        pass

    def get_platform(self):
        '''
        get system os type
        :return: os type
        '''
        os_platform = platform.system()
        return os_platform

    def collect(self):
        '''
        collect system info
        :return: system info
        '''
        os_platform = self.get_platform()
        try:
            func = getattr(self, os_platform)
            info_data = func()
            format_data = self.build_report_data(info_data)
            return format_data
        except Exception:
            sys.exit("Error: AntOps doens't support os [%s]" % os_platform)

    def Linux(self):
        '''
        use linux os deal api
        :return: result sysinfo
        '''
        sys_info = plugin_api.LinuxSysInfo()
        return sys_info

    def Windows(self):
        '''
        use windows os deal api
        :return: result sysinfo
        '''
        sys_info = plugin_api.WindowsSysInfo()
        return sys_info

    def build_report_data(self, data):
        '''
        default deal collect data
        :param data: get collect system info
        :return: deal ok data
        '''
        return data