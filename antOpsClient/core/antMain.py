#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, datetime, urllib, urllib2, json
from core import info_collection

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


    def report(self):
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()


import os, json, sys, datetime
import urllib.request, urllib.parse
from core import info_collection, api_token, Boxtqdm
from conf import settings
class ArgvHandler(object):
    def __init__(self, argvs):
        self.argvs = argvs
        self.parse_argv()
    def parse_argv(self):
        '''
        Parsing external arguments
        :return:
        '''
        if len(self.argvs) > 1:
            if hasattr(self, self.argvs[1]):
                func = getattr(self, self.argvs[1])
                func()
            else:
                self.help_msg()
        else:
            self.help_msg()
    def help_msg(self):
        msg = '''
        collect_asset
        report_asset
        '''
        print(msg)
    def collect_asset(self):
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()

    def __attach_token(self,url_str):
        '''generate md5 by token_id and username,and attach it on the url request'''
        user = settings.Params['auth']['user']
        token_id = settings.Params['auth']['token']
        md5_token,timestamp = api_token.get_token(user,token_id)
        url_arg_str = "user=%s&timestamp=%s&token=%s" %(user,timestamp,md5_token)
        if "?" in url_str:#already has arg
            new_url = url_str + "&" + url_arg_str
        else:
            new_url = url_str + "?" + url_arg_str
        return  new_url

    def load_asset_id(self, sn=None):
        asset_id_file = settings.Params['asset_id']
        has_asset_id = False
        if os.path.isfile(asset_id_file):
            asset_id = open(asset_id_file).read().strip()
            if asset_id.isdigit():
                return asset_id
            else:
                has_asset_id = False

    def __submit_data(self, url, data, method):
        if url in settings.Params['urls']:
            if type(settings.Params['port']) is int:
                url = "http://%s:%s%s" % (settings.Params['server'], settings.Params['port'], settings.Params['urls'][url])
            else:
                url = "http://%s%s" % (settings.Params['server'], settings.Params['urls'][url])
            url = self.__attach_token(url)
            print('Connecting... \n  \033[32;2m[%s] \033[0m, it may take a minute...' % url)
            if method == "get":
                args = ""
                for k, v in data.items():
                    args += "&%s=%s" % (k, v)
                args = args[1:]
                url_with_args = "%s?%s" % (url, args)
                try:
                    req = urllib.request.Request(url_with_args)
                    req_data = urllib.request.urlopen(req, timeout=settings.Params['request_timeout'])
                    callback = req_data.read()
                    print("-->server response:", callback)
                    return callback
                except urllib.request.URLError as e:
                    sys.exit("\033[31;1m%s\033[0m" % e)
            elif method == "post":
                try:
                    data_encode = urllib.parse.urlencode(data, encoding='utf-8')
                    # 解决 POST data should be bytes or an iterable of bytes. It cannot be of type str.
                    req = urllib.request.Request(url=url, data=bytes(data_encode, encoding='utf-8'))
                    res_data = urllib.request.urlopen(req, timeout=settings.Params['request_timeout'])
                    callback = res_data.read()
                    callback = str(callback, encoding='utf-8')
                    callback = json.loads(callback)
                    print(
                        "[METHOD]:\n  \033[31;1m[%s] \033[0m \n[URL]:\n  \033[31;1m[%s] \033[0m \n[RESPONSE]:\n  \033[31;1m%s \033[0m\n" % \
                        (method, url, callback))
                    return callback
                except Exception as e:
                    sys.exit("\033[31;1m%s\033[0m" % e)
            else:
                raise KeyError
    def __update_asset_id(self,new_asset_id):
        asset_id_file = settings.Params['asset_id']
        f = open(asset_id_file,"w")
        f.write(str(new_asset_id))
        f.close()
    def report_asset(self):
        obj = info_collection.InfoCollection()
        asset_data = obj.collect()
        asset_id = self.load_asset_id(asset_data["sn"]) # 只是从文件里取出asset_id
        if asset_id:
            asset_data["asset_id"] = asset_id
            post_url = "asset_report"
        else:
            asset_data["asset_id"] = None
            post_url = "asset_report_with_no_id"
        data = {"asset_data": json.dumps(asset_data)}
        response = self.__submit_data(post_url, data, method="post")
        if "asset_id" in response:
            self.__update_asset_id(response["asset_id"])
        self.log_record(response)

    def log_record(self,log,action_type=None):
        f = open(settings.Params["log_file"],"a")
        if log is str:
            pass
        if type(log) is dict:
            if "info" in log:
                for msg in log["info"]:
                    log_format = "%s\tINFO\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
            if "error" in log:
                for msg in log["error"]:
                    log_format = "%s\tERROR\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
            if "warning" in log:
                for msg in log["warning"]:
                    log_format = "%s\tWARNING\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
        f.close()
