# -*- coding: utf-8 -*-
import requests
import random
import string
import time
import json
import configparser
from  Logger import Logger
from json_compare import json_compare
from apps import apps

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")
# url = cf.get("all", "qinghua_url")
email = cf.get("auth","email")
password = cf.get("auth","qinghua_passwd")
# password = cf.get("auth","passwd")

def gettoken( email , password):
    payload = {"email": email , "password": password}
    try:
        re = requests.post(url + "/v1/login" , data=json.dumps(payload))
        # print(re.json()['data'])
        return re.json()['data']
    except:
        Logger.log_fail("Can't get token")
        return None

TOKEN = gettoken(email, password)

def assert_status_code(code,assert_code):
    if code != assert_code:
        Logger.log_fail("Response http code " + str(code) + ", but expected is "+ str(assert_code) + ".")
    else:
        Logger.log_pass("Response http code is " + str(code) + " as expected.")

def create_app(num):
    a = apps()
    Logger.log_info("Create app.")
    for i in range(1,num):
        app_id = str(random.random())
        print(app_id)
        payload = json.load(open("post_apps.json"))
        payload["id"] = app_id
        a_re_2 = a.post_apps(payload)
        assert_status_code(a_re_2[0], 201)

def delete_app():
    a = apps()
    Logger.log_info("Delete apps")
    a_re_1 = a.get_apps()
    assert_status_code(a_re_1[0], 200)
    for i in a_re_1[1]["data"]["apps"]:
        #删除应用
        app_id = i["id"][1:]
        if app_id[:2] == '0.':
            a_re_6 = a.delete_apps(app_id)
            assert_status_code(a_re_6[0], 200)


if __name__ == '__main__':
    # create_app(50)
    delete_app()

