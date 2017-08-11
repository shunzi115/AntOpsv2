#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

def check_python():
    current_python = sys.version_info
    res_data = {}
    if len(current_python) > 1:
        if current_python >= (3,):
            res_data["pversion"] = 3
        elif current_python < (3,) and current_python > (2,):
            res_data["pversion"] = 2
        else:
            res_data["pversion"] = None
    else:
        pass
    return res_data