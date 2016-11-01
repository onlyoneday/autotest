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
        print(TOKEN)
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

class metrics(object):

    def __init__(self):
        pass

    #获取集群主机列表 GET /v1/nodes   1
    def get_nodes(self):
        re = requests.get(url + "/v1/nodes",headers={'Authorization': TOKEN})
        return re.status_code ,re.json(), re.text

    #获取指定主机的信息 GET /v1/nodes/:node_ip/info   2
    def get_nodes_info(self,node_ip):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/info",headers={'Authorization': TOKEN})
        return re.status_code, re.json(), re.text

    #获取指定主机的容器列表 GET /v1/nodes/:node_ip/instances   3
    def get_nodes_instances(self,node_ip):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/instances",headers={'Authorization': TOKEN})
        return re.status_code, re.json(), re.text

    # 获取指定主机的镜像列表 GET /v1/nodes/:node_ip/images   4
    def get_nodes_images(self, node_ip):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/images", headers={'Authorization': TOKEN})
        return re.status_code, re.json(), re.text

    #获取主机上指定容器的信息 GET / v1 / nodes /:node_ip / instances /:instance_id / info   5
    def get_nodes_instanses_info(self, node_ip, instance_id):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/instances/" + instance_id + "/info", headers={'Authorization': TOKEN})
        return re.status_code, re.json(), re.text


if __name__ == '__main__':
    type = sys.argv[1]
    user = sys.argv[2]
    repeat = sys.argv[3]

    a = apps()

    m = metrics()

    def app_list(no):
        start = time.time()
        re = a.get_apps()
        # re = a.get_queue()
        end = time.time()
        time_length = end - start
        print("%s" % time_length)
        assert_status_code(re[0], 200)

    def cluster_info(no):
        start = time.time()
        re = m.get_nodes()
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
                    po.apply_async(gettoken, args=())
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
                    po.apply_async(app_list, args=(int(user),))
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
                    po.apply_async(cluster_info, args=(int(user),))
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    else:
        print("Usage: main.py login|app_list|cluster_info n(users number) n(repeat number)")