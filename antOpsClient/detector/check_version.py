#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

def check_python():
    current_python = sys.version
    list_python = current_python.split(".")
    res_data = {}
    if len(list_python) > 1:
        if list_python[0] >= 3:
            res_data["pversion"] = 3
        elif list_python[0] == 2:
            res_data["pversion"] = 2
        else:
            res_data["pversion"] = 1
    else:
        pass
    return res_data