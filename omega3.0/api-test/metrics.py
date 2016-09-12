import requests
import json
import random
import configparser
from  Logger import Logger
from json_compare import json_compare
from apps import apps

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")
email = cf.get("auth","email")
password = cf.get("auth","passwd")

def gettoken( email , password):
    payload = {"email": email , "password": password}
    try:
        re = requests.post(url + "/v1/login" , data=json.dumps(payload))
        return re.json()['data']
    except:
        Logger.log_fail("Can't get token")
        return None

TOKEN = gettoken(email, password)

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

    # 获取主机上指定容器的状态 GET /v1/nodes/:node_ip/instances/:instance_id/stats   6
    def get_nodes_instances_stats(self, node_ip, instance_id):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/instances/" + instance_id + "/stats", headers={'Authorization': TOKEN}, stream=True)
        index = 0
        lines = []
        for line in re.iter_lines():
            if line:
                lines.append(line)
                index += 1
            if index == 4:
                break
        code = re.status_code
        re.close()
        return code, lines

    #获取主机上指定容器的日志 GET /v1/nodes/:node_ip/instances/:instance_id/logs    7
    def get_nodes_instances_logs(self, node_ip, instance_id):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/instances/" + instance_id + "/logs", headers={'Authorization': TOKEN}, stream=True)
        index = 0
        lines = []
        for line in re.iter_lines():
            if line:
                lines.append(line)
                index += 1
            if index == 4:
                break
        code = re.status_code
        re.close()
        return code, lines


def assert_status_code(code,assert_code):
    if code != assert_code:
        Logger.log_fail("Response http code " + str(code) + ", but expected is "+ str(assert_code) + ".")
    else:
        Logger.log_pass("Response http code is " + str(code) + " as expected.")

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
    print(TOKEN)
    m = metrics()
    #获取集群主机列表 GET /v1/nodes==============================================       1
    re = m.get_nodes()

    #测试GET /v1/nodes/返回的http_code
    Logger.log_info("1. Test get nodes response http code")
    assert_status_code(re[0], 200)

    #测试GET /v1/nodes/返回的data中的元素
    Logger.log_info("2. Test get nodes reponse json")
    json_compare(re[1]["data"], "metrics.json", "GET /v1/nodes/")

    print(re[2])

    #获取指定主机的信息 GET /v1/nodes/:node_ip/info==================================      2
    # 测试 ip 为 master 时 GET /v1/nodes/:node_ip/info返回的http_code
    Logger.log_info("3. Test get nodes info response http code with master ip")
    master_ip = re[1]["data"]["masters"][0].get('ip', None)

    re2 = m.get_nodes_info(master_ip)
    assert_status_code(re2[0], 200)

    # 测试 GET /v1/nodes/:node_ip/info 中的元素 - master_ip
    Logger.log_info("4. Test get node info reponse json with master ip")
    json_compare(re2[1]["data"], "metrics.json", "GET /v1/nodes/:node_ip/info")

    print(re2[2])

    # 测试 ip 为 slave 时 GET /v1/nodes/:node_ip/info返回的http_code
    Logger.log_info("5. Test get nodes info response http code with slave ip")
    slave_ip = re[1]["data"]["slaves"][0].get('ip', None)

    re2 = m.get_nodes_info(master_ip)
    assert_status_code(re2[0], 200)

    # 测试 GET /v1/nodes/:node_ip/info 中的元素 - slave_ip
    Logger.log_info("6. Test get node info reponse json with slave ip")
    json_compare(re2[1]["data"], "metrics.json", "GET /v1/nodes/:node_ip/info")

    print(re2[2])

    #测试 ip 不存在时 GET /v1/nodes/:node_ip/info返回的http_code
    Logger.log_info("7. Test get nodes info response http code with invalid ip")
    re2 = m.get_nodes_info("192.168.1.1")
    assert_status_code(re2[0], 404)


    #获取指定主机的容器列表 GET /v1/nodes/:node_ip/instances==================================     3
    # 测试 ip 为 master 时  GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("8. Test get nodes instances response http code with master ip")
    re3 = m.get_nodes_instances(master_ip)
    assert_status_code(re3[0], 200)

    master_instance_id = re3[1]["data"][0]["Id"]
    print("master_instance_id:")
    print(master_instance_id)

    # # 测试 ip 为 master 时  GET /v1/nodes/:node_ip/instances 返回的response json
    Logger.log_info("9. Test get nodes instances response json with master ip")
    json_compare(re3[1]["data"], "metrics.json", "GET /v1/nodes/:node_ip/instances")

    print(re3[2])

    # 测试 ip 为 slave 时  GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("10. Test get nodes instances response json with slave ip")
    re3 = m.get_nodes_instances(slave_ip)
    assert_status_code(re3[0], 200)
    try:
        slave_instance_id = re3[1]["data"][0]["Id"]
    except:
        Logger.log_fail("Can't get slave_instance_id")

    # 测试 ip 为 slave 时  GET /v1/nodes/:node_ip/instances 返回的response json
    Logger.log_info("11. Test get nodes instances response json with slave ip")
    json_compare(re3[1]["data"], "metrics.json", "GET /v1/nodes/:node_ip/instances")
    print(re3[2])

    # 测试 ip 不存在时 GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("12. Test get nodes instances response http code with invalid ip")
    re3 = m.get_nodes_instances("192.168.1.1")
    assert_status_code(re3[0], 404)

    # 获取指定主机的镜像列表 GET /v1/nodes/:node_ip/images==================================        4
    # 测试 ip 为 master 时  GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("13. Test get nodes images response http code with master ip")
    re4 = m.get_nodes_images(master_ip)
    assert_status_code(re4[0], 200)

    # # 测试 ip 为 master 时  GET /v1/nodes/:node_ip/instances 返回的response json
    Logger.log_info("14. Test get nodes images response json with master ip")
    json_compare(re4[1]["data"], "metrics.json", "GET /v1/nodes/:node_ip/images")
    print(re4[2])

    # 测试 ip 为 slave 时  GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("15. Test get nodes images response json with slave ip")
    re4 = m.get_nodes_images(slave_ip)
    assert_status_code(re4[0], 200)

    # 测试 ip 为 slave 时  GET /v1/nodes/:node_ip/instances 返回的response json
    Logger.log_info("16. Test get nodes images response json with slave ip")
    json_compare(re4[1]["data"], "metrics.json", "GET /v1/nodes/:node_ip/images")
    print(re4[2])

    # 测试 ip 不存在时 GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("17. Test get nodes images response http code with invalid ip")
    re4 = m.get_nodes_instances("192.168.1.1")
    assert_status_code(re4[0], 404)

    # 获取主机上指定容器的信息 GET / v1 / nodes /:node_ip / instances /:instance_id / info============    5
    # Test get nodes instances info response http code with master instanse ip
    Logger.log_info("18. Test get nodes instances info response http code with master instanse ip")
    re5 = m.get_nodes_instanses_info(master_ip,master_instance_id)
    assert_status_code(re5[0], 200)

    # 获取主机上指定容器的状态 GET /v1/nodes/:node_ip/instances/:instance_id/stats===================    6
    re_6 = m.get_nodes_instances_stats(master_ip,master_instance_id)

    Logger.log_info("19. Test get instance status by id response http code.")
    assert_status_code(re_6[0], 200)

    Logger.log_info("20. Test get instance status by id response json.")
    lines = re_6[1]
    for line in lines:
        str_line = line.decode("utf-8")
        if str_line != 'event:container-stats':
            str_line = str_line[5:]
            json_line = json.loads(str_line)
            print(str_line)
            json_compare(json_line, "metrics.json", "GET /v1/nodes/:node_ip/instances/:instance_id/stats")

    re_6 = m.get_nodes_instances_stats(master_ip,"invalid_id")
    Logger.log_info("21. Test get instance status by invalid id response http code.")
    assert_status_code(re_6[0], 404)
    print(re_6[1])

    #获取主机上指定容器的日志 GET /v1/nodes/:node_ip/instances/:instance_id/logs==================         7
    #先找到非swarm的slave ip
    re = m.get_nodes()
    for slave in re[1]["data"]["slaves"]:
        try:
            if slave["attributes"].get("type",None) != 'swarm':
                slave_notswarm_ip = slave["hostname"]
                break
        except:
            slave_notswarm_ip = slave["hostname"]
            break
    # print(slave_notswarm_ip)


    app_id = str(random.random())

    payload = json.load(open("post_apps_slave_ip.json"))
    payload["id"] = app_id
    # print("app_id")
    # print(app_id)
    payload["constraints"] = [["hostname","LIKE",str(slave_notswarm_ip)]]
    # print("payload")
    # print(payload)
    a = apps()
    a_re = a.post_apps(payload)

    #找到lable为app_id的instance
    re_i = m.get_nodes_instances(slave_notswarm_ip)
    # print("get_nodes_instances")
    # print(re_i[2])

    flag = 0
    for instance in re_i[1]["data"]:
        try:
            # print("APP_ID")
            # print(instance["Labels"]["APP_ID"])
            if instance["Labels"]["APP_ID"] == app_id:
                flag = 1
                # print(instance["Labels"]["APP_ID"])

                Logger.log_info("22. Test get instance logs by id response http code.")

                instance_id = instance["Id"]

                re_7 = m.get_nodes_instances_logs(slave_notswarm_ip,instance_id)
                # print(re_7[1])

                assert_status_code(re_7[0], 200)

                # Logger.log_info("23.Test get instance logs by id response json")
                # lines = re_7[1]
                # for line in lines:
                #     str_line = line.decode("utf-8")
                #     if str_line != 'event:container-logs':
                #         str_line = str_line[5:]
                #         json_line = json.loads(str_line)
                #         json_compare(json_line, "metrics.json", "GET /v1/nodes/:node_ip/instances/:instance_id/stats")
        except:
            pass
    if flag == 0:
        Logger.log_fail("Can't find instance.")

    re_7 = m.get_nodes_instances_logs(master_ip, "invalid_id")
    Logger.log_info("24. Test get instance logs by invalid id response http code.")
    assert_status_code(re_7[0], 404)

    delete_app()





