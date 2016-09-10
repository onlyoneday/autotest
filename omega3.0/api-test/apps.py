# -*- coding: utf-8 -*-
import requests
import random
import string
import time
import json
import configparser
from  Logger import Logger
from json_compare import json_compare

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")
email = cf.get("auth","email")
password = cf.get("auth","passwd")

def gettoken( email , password):
    payload = {"email": email , "password": password}
    try:
        re = requests.post(url + "/v1/login" , data=json.dumps(payload))
        print(re.json()['data'])
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

if __name__ == '__main__':
    a = apps()

    app_id = str(random.random())
    print(app_id)

    # 新建应用 POST /v1/apps==============================================      2
    payload = json.load(open("post_apps.json"))
    payload["id"] = app_id
    a_re_2 = a.post_apps(payload)

    Logger.log_info("1. Test post apps response http code.")
    assert_status_code(a_re_2[0], 201)


    Logger.log_info("2. Test post apps response json.")
    json_compare(a_re_2[1]["data"], "apps.json", "POST /v1/apps")
    print(a_re_2[2])


    Logger.log_info("3. Test post apps response httpcode with duplicate app id.")
    a_re_2 = a.post_apps(app_id)
    assert_status_code(a_re_2[0], 400)

    # 获取应用列表 GET /v1/apps ==============================================      1
    a_re_1 = a.get_apps()


    Logger.log_info("4. Test get apps response http code.")
    assert_status_code(a_re_1[0], 200)


    Logger.log_info("5. Test get apps response json.")
    json_compare(a_re_1[1]["data"], "apps.json", "GET /v1/apps")
    print(a_re_1[2])

    # 获取指定应用的信息 GET /v1/apps/:aid======================================     3
    time.sleep(5)
    a_re_3 = a.get_apps_aid(app_id)

    Logger.log_info("6. Test get apps by aid response http code.")
    assert_status_code(a_re_3[0], 200)

    Logger.log_info("7. Test get apps by aid response json.")
    json_compare(a_re_3[1]["data"], "apps.json", "GET /v1/apps/:aid")
    print(a_re_3[2])

    Logger.log_info("8. Test get apps by aid response http code with invalid aid.")
    a_re_3 = a.get_apps_aid("invalid_aid")
    assert_status_code(a_re_3[0], 400)

    # 获取指定应用的状态 GET /v1/apps/:aid/stats=================================     4
    a_re_4 = a.get_apps_stats(app_id)

    Logger.log_info("9. Test get apps status by aid response http code.")
    assert_status_code(a_re_4[0], 200)

    Logger.log_info("10. Test get apps status by aid response json.")
    lines = a_re_4[1]
    for line in lines:
        str_line = line.decode("utf-8")
        if str_line != 'event:app-stats':
            str_line = str_line[5:]
            print(str_line)
            json_line = json.loads(str_line)
            print(type(json_line))
            json_compare(json_line,"apps.json","GET /v1/apps/:aid/stats")

    a_re_4 = a.get_apps_stats("invalid_aid")
    Logger.log_info("11. Test get apps status by invalid aid response http code.")
    assert_status_code(a_re_4[0], 404)


    # 获取指定应用所有实例 GET /v1/apps/:aid/tasks===============================     8
    a_re_8 = a.get_apps_tasks(app_id)

    Logger.log_info("12. Test get apps tasks by aid response http code.")
    assert_status_code(a_re_8[0], 200)

    Logger.log_info("13. Test get apps tasks by aid response json.")
    json_compare(a_re_8[1]["data"], "apps.json", "GET /v1/apps/:aid/tasks")
    print(a_re_8[2])

    Logger.log_info("14. Test get apps by tasks aid response http code with invalid aid.")
    a_re_8 = a.get_apps_tasks("invalid_aid")
    assert_status_code(a_re_8[0], 400)

    # 获取指定应用所有版本ID GET /v1/apps/:aid/versions==========================     9
    a_re_9 = a.get_apps_versions(app_id)
    version_id = a_re_9[1]["data"]["versions"][0]
    print(version_id)

    Logger.log_info("15. Test get apps versions by aid response http code.")
    assert_status_code(a_re_9[0], 200)

    Logger.log_info("16. Test get apps versions by aid response json.")
    json_compare(a_re_9[1]["data"], "apps.json", "GET /v1/apps/:aid/versions")
    print(a_re_9[2])

    Logger.log_info("17. Test get apps by versions aid response http code with invalid aid.")
    a_re_9 = a.get_apps_tasks("invalid_aid")
    assert_status_code(a_re_9[0], 400)

    # 根据应用版本id获取版本信息GET /v1/apps/:aid/versions/:version===============     10
    a_re_10 = a.get_apps_versions_versionid(app_id,version_id)

    Logger.log_info("18. Test get apps versions by aid response http code.")
    assert_status_code(a_re_10[0], 200)

    Logger.log_info("19. Test get apps versions by aid response json.")
    json_compare(a_re_10[1]["data"], "apps.json", "GET /v1/apps/:aid/versions/:version")
    print(a_re_10[2])

    Logger.log_info("20. Test get apps by versions aid response http code with invalid aid.")
    a_re_10 = a.get_apps_versions_versionid("invalid_aid","xxxx-xxxx")
    assert_status_code(a_re_10[0], 400)

    # 更新指定应用 PUT /v1/apps/:aid============================================      5
    payload = json.load(open("put_apps.json"))
    payload["id"] = app_id
    a_re_5 = a.put_apps(app_id,payload)

    Logger.log_info("21. Test update apps by aid response http code.")
    assert_status_code(a_re_5[0], 200)

    Logger.log_info("22. Test update apps by aid response json.")
    json_compare(a_re_5[1]["data"], "apps.json", "PUT /v1/apps/:aid")
    print(a_re_5[2])

    Logger.log_info("23. Test update apps by aid response http code with invalid aid.")
    a_re_5 = a.put_apps("invalid_aid",payload)
    assert_status_code(a_re_5[0], 400)


    # 重启一个应用 POST /v1/apps/:aid/restart===================================      7
    a_re_7 = a.post_apps_restart(app_id)

    Logger.log_info("24. Test restart apps by aid response http code.")
    assert_status_code(a_re_7[0], 200)

    Logger.log_info("25. Test restart apps by aid response json.")
    json_compare(a_re_7[1]["data"], "apps.json", "PUT /v1/apps/:aid")
    print(a_re_7[2])

    Logger.log_info("26. Test restart apps by aid response http code with invalid aid.")
    a_re_7 = a.post_apps_restart("invalid_aid")
    assert_status_code(a_re_7[0], 400)


    # 删除指定应用 DELETE /v1/apps/:aid=========================================      6
    # a_re_6 = a.delete_apps(app_id)
    #
    # Logger.log_info("27. Test delete apps response http code.")
    # assert_status_code(a_re_6[0], 200)
    # print(a_re_6)

    # 列出所有等待执行的任务实例POST /v1/queue====================================      12