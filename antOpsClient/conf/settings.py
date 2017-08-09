#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Params = {
    "server": "10.1.2.102",
    "port": 8080,
    "request_tiemout": 30,
    "urls": {
        "asset_report": "/cmdb/report",
        "asset_update": "/cmdb/update",
    },
    "asset_id": "%s/var/.asset_id" % base_dir,
    "log_file": "%s/logs/run_log" % base_dir,
}