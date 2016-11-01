# -*- coding: utf-8 -*-
import requests
import random
import string
import time
import json
from  Logger import Logger
import sys
# from json_compare import json_compare
# from apps import apps

url = "http://127.0.0.1:9999"

def gettoken():
    payload = {"userName": "cc", "password": "111111cC"}
    try:
        re = requests.post(url + "/v1/login" , data=json.dumps(payload))
        # print(re.json())
        # print(re.json()['data'])
        return re.json()['data']
    except:
        Logger.log_fail("Can't get token")
        return None

TOKEN = gettoken()
print(TOKEN)

class apps(object):

    def __init__(self):
        pass

    # 获取应用列表 GET /v1/apps    1
    def get_apps(self):
        re = requests.get(url + "/v1/apps",headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    # 新建应用 POST /v1/apps      2
    def post_apps(self,payload):
        re = requests.post(url + "/v1/apps",headers={'Authorization': TOKEN}, data = json.dumps(payload))
        # print(TOKEN)
        print(re)
        return re.status_code ,re.json(), re.text

    # 获取指定应用的信息 GET /v1/apps/:aid      3
    def get_apps_aid(self,aid):
        re = requests.get(url + "/v1/apps/" + aid, headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    # 获取指定应用的状态 GET /v1/apps/:aid/stats         4
    def get_apps_stats(self, aid):
        re = requests.get(url + "/v1/apps/" + aid + "/stats", headers={'Authorization': TOKEN}, stream = True)
        index = 0
        lines = []
        for line in re.iter_lines():
            if line:
                lines.append(line)
                index+=1
            if index == 4:
                break
        code = re.status_code
        re.close()
        return code, lines

    # 更新指定应用 PUT /v1/apps/:aid       5
    def put_apps(self, aid, payload):
        payload = json.load(open("put_apps.json"))
        re = requests.put(url + "/v1/apps/" + aid, headers={'Authorization': TOKEN}, data = json.dumps(payload))
        return re.status_code, re.json(), re.text

    # 删除指定应用 DELETE /v1/apps/:aid       6
    def delete_apps(self,aid):
        re = requests.delete(url + "/v1/apps/" + aid,headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    # 重启一个应用 POST /v1/apps/:aid/restart        7
    def post_apps_restart(self,aid):
        re = requests.post(url + "/v1/apps/" + aid + "/restart",headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    # 获取指定应用所有实例 GET /v1/apps/:aid/tasks      8
    def get_apps_tasks(self, aid):
        re = requests.get(url + "/v1/apps/" + aid + "/tasks", headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    # 获取指定应用所有版本ID GET /v1/apps/:aid/versions      9
    def get_apps_versions(self, aid):
        re = requests.get(url + "/v1/apps/" + aid + "/versions", headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    # 根据应用版本id获取版本信息GET /v1/apps/:aid/versions/:version      10
    def get_apps_versions_versionid(self, aid, version_id):
        re = requests.get(url + "/v1/apps/" + aid + "/versions/" + version_id, headers={'Authorization': TOKEN})
        return re.status_code, re.json(), re.text

    # 杀掉列出的任务实例并根据请求扩缩应用 POST /v1/tasks/delete      11
    def post_tasks_delete(self, ids):
        str = '{"ids":[' + ids +']}'
        payload = str.json()
        re = requests.post(url + "/v1/tasks/delete/" + ids,headers={'Authorization': TOKEN}, data=payload)
        return re.status_code ,re.json(), re.text

    # 列出所有等待执行的任务实例POST /v1/queue      12
    def get_queue(self):
        re = requests.get(url + "/v1/queue", headers={'Authorization': TOKEN})
        return re.status_code, re.json(), re.text

def assert_status_code(code,assert_code):
    if code != assert_code:
        Logger.log_fail("Response http code " + str(code) + ", but expected is "+ str(assert_code) + ".")
    else:
        Logger.log_pass("Response http code is " + str(code) + " as expected.")

def create_app(num):
    a = apps()
    Logger.log_info("Create app.")
    for i in range(1,num+1):
        app_id = str(random.random())
        # print(app_id)
        payload = json.load(open("post_app_new.json"))
        payload["id"] = payload["id"] + app_id
        # payload["container"]["docker"]["image"] = "offlineregistry.dataman-inc.com:5000/library/2048"
        a_re_2 = a.post_apps(payload)
        assert_status_code(a_re_2[0], 201)
        print(a_re_2)

def delete_app():
    a = apps()
    Logger.log_info("Delete apps")
    a_re_1 = a.get_apps()
    # print(a_re_1[2])
    assert_status_code(a_re_1[0], 200)
    for i in a_re_1[1]["data"]["apps"]:
        #删除应用
        # print(i)
        app_id = i["id"][1:]
        # print(app_id)
        if 'test-10.' in app_id:
        # if True:
            a_re_6 = a.delete_apps(app_id)
            # print(app_id)
            # a_re_6 = a.delete_apps("xxx")
            # print(app_id)
            assert_status_code(a_re_6[0], 200)


if __name__ == '__main__':
    type = sys.argv[1]

    if type == "create":
        num = sys.argv[2]
        create_app(int(num))
    elif type == "delete":
        delete_app()
    else:
        print("Usage: deploy_apps.py create n(app number)|delete")