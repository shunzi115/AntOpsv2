#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
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
        getcmd = __import__("commands")
        linux_info = deal_sysinfo.collect_deal(getcmd)
    else:
        sys.exit("System is not found python command...")
    return linux_info