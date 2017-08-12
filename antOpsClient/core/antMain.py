#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, datetime, json
from core import info_collection
from conf import settings

# import check python version model
from plugins.detector import check_version

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
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()

    def __load_asset_id(self):
        '''
        deal local asset_id
        :return: asset_id
        '''
        asset_id_file = settings.Params["asset_id"]
        has_asset_id = False
        if os.path.isfile(asset_id_file):
            asset_id = open(asset_id_file).read().strip()
            asset_id = int(asset_id)
            if asset_id.isdigit():
                return asset_id
            else:
                has_asset_id = False

    def __import_model(self, cmd1, cmd2):
        '''
        deal urllib request command
        :param cmd1: urllib py3 or urllib2 py2 request comand
        :param cmd2: urllib.parse py3 or urllib py2  comand
        :return: return request command and urlencode command
        '''
        cmd_urllib1 = __import__(cmd1)
        cmd_urllib2 = __import__(cmd2)
        return cmd_urllib1, cmd_urllib2

    def __deal_urllib(self, cmd_urllib1, cmd_urllib2, url, data=None, pyversion=None, method=None):
        '''
        deal python2 or python3 urllib request
        :param cmd_urllib1: urllib request model
        :param cmd_urllib2: urllib urlencode model
        :param url: antOps server url
        :param data: system info data
        :param pyversion: python version
        :param method: get or post
        :return: return server callback info
        '''
        if method == "get":
            req = cmd_urllib1.Request(url)
            res_data = cmd_urllib1.urlOpen(req, timeout=settings.Params["request_timeout"])
            callback = res_data.read()
            print("--->server response: ", callback)
            return callback
        elif method =="post":
            data_encode = cmd_urllib2.urlencode(data, encoding='utf-8')
            if pyversion == 3:
                # 解决 POST data should be bytes or an iterable of bytes. It cannot be of type str.
                #  # 这里需要测试，存在bug
                req = cmd_urllib1.request.Request(url=url, data=bytes(data_encode, encoding='utf-8')) # python 3.x version
                res_data = cmd_urllib1.urlOpen(req, timeout=settings.Params["request_timeout"])
                callback = res_data.read()
                callback = str(callback, encoding='utf-8')
            elif pyversion == 2:
                req = cmd_urllib1.Request(url=url, data=data_encode)
                res_data = cmd_urllib1.urlOpen(req, timeout=settings.Params["request_timeout"])
                callback = res_data.read()
            callback = json.load(callback)
            print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" % (method, url, callback))
            return callback

    def __submit_data(self, url, data, method):
        '''
        This model is compability python2 and python3
        :param url: antOps server url
        :param data: system info data
        :param method: get or post
        :return: return server callback info
        '''
        if url in settings.Params["urls"]:
            if type(settings.Params["port"]) is int:
                url = "http://%s:%s%s" % (
                    settings.Params["server"], settings.Params["port"], settings.Params["urls"][url])
            else:
                url = "http://%s/%s" % (settings.Params["server"], settings.Params["urls"][url])
            print("Connectins.. \n \033[32;2m[%s] \033[0m, it may take a minute..." % url)
            if method == "get":
                args = ""
                for k, v in data.items():
                    args += "&%s=%s" % (k, v)
                args = args[1:]
                url_with_args = "%s?%s" % (url, args)
                try:
                    pversion = check_version.check_python()
                    if pversion == 3:
                        cmd_urllib1, cmd_urllib2 = self.__import_model("urllib.request", "urllib.parse")
                        callback = self.__deal_urllib(cmd_urllib1, cmd_urllib2, url_with_args, method="get")
                        return callback
                    elif pversion == 2:
                        cmd_urllib1, cmd_urllib2 = self.__import_model("urllib2", "urllib")
                        callback = self.__deal_urllib(cmd_urllib1, cmd_urllib2, url_with_args, method="get")
                        return callback
                except cmd_urllib1.request.URLError:
                    sys.exit("\033[31;1m%s\033[0m" % cmd_urllib1.request.URLError)
            elif method == "post":
                try:
                    pversion = check_version.check_python()
                    if pversion == 3:
                        cmd_urllib1, cmd_urllib2 = self.__import_model("urllib.request", "urllib.parse")
                        callback = self.__deal_urllib(cmd_urllib1, cmd_urllib2, url, data=data, pyversion=pversion, method="get")
                        return callback
                    elif pversion == 2:
                        cmd_urllib1, cmd_urllib2 = self.__import_model("urllib2", "urllib")
                        callback = self.__deal_urllib(cmd_urllib1, cmd_urllib2, url, data=data, pyversion=pversion, method="get")
                        return callback
                except Exception:
                    sys.exit("\033[31;1m%s\033[0m" % Exception)
            else:
                raise KeyError

    def __update_asset_id(self, asset_id):
        asset_id_file = settings.Params["asset_id"]
        f = open(asset_id_file, "w")
        f.write(str(asset_id))
        f.close()

    def report(self):
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()
        asset_id = self.__load_asset_id() # load from asset_id file
        if asset_id:
            asset_data["asset_id"] = asset_id
            post_url = "asset_update"
        else:
            asset_data["asset_id"] = None
            post_url = "asset_report"
        data = {"asset_data": json.dumps(asset_data)}
        response = self.__submit_data(post_url, data, method="post")
        if "asset_id" in response:
            self.__update_asset_id(response["asset_id"])
        self.log_record(response)

    def log_record(self, log_mesg):
        '''
        log deal model
        :param log_mesg: server callback info
        :return: None
        '''
        f = open(settings.Params["log_file"], "a")
        if log_mesg is str:
            pass
        if type(log_mesg) is dict:
            if "info" in log_mesg:
                for msg in log_mesg["info"]:
                    log_format = "%s\tINFO\t%s\n" % (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), msg)
                    f.write(log_format)
            if "error" in log_mesg:
                for msg in log_mesg["error"]:
                    log_format = "%s\tERROR\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
            if "warning" in log_mesg:
                for msg in log_mesg["warning"]:
                    log_format = "%s\tWARNING\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
        f.close()