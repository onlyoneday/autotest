# -*- coding: utf-8 -*-
import requests
import random
import string
import time
import sys
import json

from  Logger import Logger
# from json_compare import json_compare
import multiprocessing
from multiprocessing import Pool

url = "http://192.168.1.118:81/ui"

def gettoken():
    payload = {"userName":"admin","password":"dataman1234"}
    try:

        re = requests.post(url + "/v1/login" , data=json.dumps(payload))

        print(re.json())

        return re.json()['data']
    except:
        Logger.log_fail("Can't get token")
        return None

TOKEN = gettoken()
print("---------------------------")


def get_app_page():
    start_time = time.time()
    try:
        re = requests.get(url + "/static/js/angular.75276ac6.js",headers={'Authorization': TOKEN})
        re = requests.get(url + "/static/bower_components/ace-builds/src/ace.js", headers={'Authorization': TOKEN})
        re = requests.get(url + "/static/js/template.9b8b3fcc.js", headers={'Authorization': TOKEN})
    except Exception as e:
        print(e)
    finally:
        end_time = time.time()
    time_length = end_time - start_time
    print(time_length)

def get_home_page():
    pass

def get_cluster_info():
    pass

if __name__ == '__main__':
    type = sys.argv[1]
    user = sys.argv[2]
    repeat = sys.argv[3]

    # ====================
    if type == "login":
        for i in range(1, int(repeat) + 1):
            po = Pool()
            for i in range(1, int(user) + 1):
                try:
                    po.apply_async(get_home_page, args=())
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    # ====================
    elif type == "app_list":
        for i in range(1, int(repeat) + 1):
            po = Pool()
            for i in range(1, int(user) + 1):
                try:
                    po.apply_async(get_app_page, args=())
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    # ====================
    elif type == "cluster_info":
        for i in range(1, int(repeat) + 1):
            # print("start")
            po = Pool()
            for i in range(1, int(user) + 1):
                try:
                    po.apply_async(get_cluster_info, args=())
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    else:
        print("Usage: main.py login|app_list|cluster_info n(users number) n(repeat number)")