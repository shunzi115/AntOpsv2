#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, json, datetime


class ArgvHandler(object):
    def __init__(self, argvs):
        self.argvs = argvs
        self.parse_argv()

    def parse_argv(self):
        if len(self.argvs) > 1:
            if hasattr(self, self.argvs[1]):
                func = getattr(self, self.argvs[1])
                func()
            else:
                self.help()
        else:
            self.help()

    def help(self):
        msg = '''
        collect
        report
        '''
        print(msg)

    def collect(self):
        pass

    def report(self):
        pass