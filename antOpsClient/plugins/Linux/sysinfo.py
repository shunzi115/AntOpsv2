#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, subprocess, socket
import re

# import check python version model
from plugins.detector import check_version

# import deal and collect linux system info model
from . import deal_sysinfo

def collect():
    pversion = check_version.check_python()
    if pversion["pversion"] == 3:
        getcmd = __import__("subprocess")
        linux_info = deal_sysinfo.collect_deal(getcmd)
    elif pversion["pversion"] == 2:
        getcmd = __import__("subprocess")
        linux_info = deal_sysinfo.collect_deal(getcmd)
    return linux_info


# class DiskPlugin(object):
#     def __init__(self,getcmd):
#         self.getcmd = getcmd
#
#     def linux(self):
#         result = {'physical_disk_driver':[]}
#         try:
#             script_path = os.path.dirname(os.path.abspath(__file__))
#             shell_command = " %s/MegaCli  -PDList -aALL" % script_path
#             output = self.getcmd.get(shell_command)
#             result['physical_disk_driver'] = self.parse(output[1])
#         except Exception as e:
#             result['error'] = e
#         return result
#
#     def parse(self,content):
#         '''
#         解析shell命令返回结果
#         :param content: shell 命令结果
#         :return:解析后的结果
#         '''
#         response = []
#         result = []
#         for row_line in content.split("\n\n\n\n"):
#             result.append(row_line)
#         for item in result:
#             temp_dict = {}
#             for row in item.split('\n'):
#                 if not row.strip():
#                     continue
#                 if len(row.split(':')) != 2:
#                     continue
#                 key,value = row.split(':')
#                 name =self.mega_patter_match(key);
#                 if name:
#                     if key == 'Raw Size':
#                         raw_size = re.search('(\d+\.\d+)',value.strip())
#                         if raw_size:
#                             temp_dict[name] = raw_size.group()
#                         else:
#                             raw_size = '0'
#                     else:
#                         temp_dict[name] = value.strip()
#             if temp_dict:
#                 response.append(temp_dict)
#         return response
#
#     def mega_patter_match(self,needle):
#         grep_pattern = {'Slot':'slot', 'Raw Size':'capacity', 'Inquiry':'model', 'PD Type':'iface_type'}
#         for key,value in grep_pattern.items():
#             if needle.startswith(key):
#                 return value
#         return False

