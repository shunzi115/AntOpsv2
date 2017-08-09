#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == "__main__":
    from core import antMain
    antMain.ArgvHandler(sys.argv)