# -*- coding: utf-8 -*-
import requests
import random
import string
import time
import sys
import json
from  Logger import Logger
import multiprocessing
from multiprocessing import Pool

url = "http://192.168.1.118:81"

def gettoken():
    payload = {"userName": "admin" , "password": "dataman1234"}
    try:
        start_login = time.time()
        re = requests.post(url + "/v1/login" , data=json.dumps(payload))
        end_login = time.time()
        # print(re.json()['data'])
        time_length = end_login - start_login
        print("%s" % time_length)
        return re.json()['data']
    except:
        Logger.log_fail("Can't get token")
        return None

TOKEN = gettoken()
print("---------------------------")

def assert_status_code(code,assert_code):
    if code != assert_code:
        Logger.log_fail("Response http code " + str(code) + ", but expected is "+ str(assert_code) + ".")
    # else:
        # Logger.log_pass("Response http code is " + str(code) + " as expected.")

if __name__ == '__main__':
    type = sys.argv[1]
    user = sys.argv[2]
    repeat = sys.argv[3]



    def app_list():
        start = time.time()
        re = requests.get(url + "/static/js/angular.75276ac6.js",headers={'Authorization': TOKEN})
        # re = requests.get(url + "/static/bower_components/ace-builds/src/ace.js", headers={'Authorization': TOKEN})
        # re = requests.get(url + "/static/js/template.9b8b3fcc.js", headers={'Authorization': TOKEN})
        end = time.time()
        time_length = end - start
        print("%s" % time_length)
        assert_status_code(re[0], 200)

    def cluster_info():
        start = time.time()
        # re = m.get_nodes()
        end = time.time()
        time_length = end - start
        print("%s" % time_length)
        assert_status_code(re[0], 200)

    def get_home_page():
        start = time.time()
        re = requests.get(url + "/static/css/style.f1698070.css", headers={'Authorization': TOKEN})
        # re = requests.get(url + "/static/js/angular.75276ac6.js",headers={'Authorization': TOKEN})
        end = time.time()
        time_length = end - start
        print("%s" % time_length)
        assert_status_code(re[0], 200)

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
                    po.apply_async(app_list, args=())
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
                    po.apply_async(cluster_info, args=())
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    else:
        print("Usage: main.py login|app_list|cluster_info n(users number) n(repeat number)")