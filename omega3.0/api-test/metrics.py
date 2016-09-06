import requests
import json
import configparser
from  auth_api import authapi
from  Logger import Logger
from json_compare import json_compare

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")

def gettoken( email , password):
    payload = {"email": email , "password": password}
    re = requests.post(url + "/v1/login" , data=json.dumps(payload))
    return re.json()['data']

class metrics(object):

    def __init__(self):
        l = authapi()
        self.token = gettoken('admin@dataman-inc.com', 'Dataman1234')

    #获取集群主机列表 /v1/nodes
    def get_nodes(self):
        re = requests.get(url + "/v1/nodes",headers={'Authorization': self.token})
        return re.status_code ,re.json()

    #获取指定主机的信息 /v1/nodes/:node_ip/info
    def get_nodes_info(self,node_ip):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/info",headers={'Authorization': self.token})
        return re.status_code, re.json()

    #获取指定主机的容器列表 /v1/nodes/:node_ip/instances
    def get_nodes_instances(self,node_ip):
        re = requests.get(url + "/v1/nodes/" + node_ip + "/instances",headers={'Authorization': self.token})
        return re.status_code, re.json()


def assert_status_code(re,assert_code):
    if re[0] != assert_code:
        Logger.log_fail("Response http code " + str(re[0]) + ", but expected is "+ str(assert_code) + ".")
    else:
        Logger.log_pass("Response http code is " + str(assert_code) + " as expected.")

if __name__ == '__main__':
    #GET /v1/nodes/ 测试===获取集群主机列表 /v1/nodes==============================================
    m = metrics()
    re = m.get_nodes()

    #测试GET /v1/nodes/返回的http_code
    Logger.log_info("Test get nodes response http code")
    assert_status_code(re, 200)

    #测试GET /v1/nodes/返回的data中的元素
    Logger.log_info("Test get nodes reponse json")
    if re[1]["data"].get('masters',None) == None:
        Logger.log_fail("Get /v1/node data don't include masters")
    elif re[1]["data"].get('slaves',None) == None:
        Logger.log_fail("Get /v1/node data don't include slaves")
    elif re[1]["data"]["masters"][0].get('id',None) == None:
        Logger.log_fail("Get /v1/node data don't include master-id")
    elif re[1]["data"]["masters"][0].get('ip',None) == None:
        Logger.log_fail("Get /v1/node data don't include master-ip")
    else:
        Logger.log_pass("Get /v1/node reponse json is correct")

    # GET /v1/nodes/:node_ip/info 测试 - 获取master ===获取指定主机的信息 /v1/nodes/:node_ip/info==================================
    # 测试 ip 为 master 时 GET /v1/nodes/:node_ip/info返回的http_code
    Logger.log_info("Test get nodes info response http code with master ip")
    master_ip = re[1]["data"]["masters"][0].get('ip', None)
    re2 = m.get_nodes_info(master_ip)
    assert_status_code(re2, 200)

    # 测试 GET /v1/nodes/:node_ip/info 中的元素
    Logger.log_info("Test get node info reponse json")
    json_compare(re2[1]["data"], "api_response.json", "GET /v1/nodes/:node_ip/info")

    # 测试 ip 为 slave 时 GET /v1/nodes/:node_ip/info返回的http_code
    Logger.log_info("Test get nodes info response http code with slave ip")
    slave_ip = re[1]["data"]["slaves"][0].get('ip', None)
    re2 = m.get_nodes_info(master_ip)
    assert_status_code(re2, 200)

    #测试 ip 不存在时 GET /v1/nodes/:node_ip/info返回的http_code
    Logger.log_info("Test get nodes info response http code with invalid ip")
    re2 = m.get_nodes_info("192.168.1.1")
    assert_status_code(re2, 404)

    # GET /v1/nodes/:node_ip/instances===获取指定主机的容器列表 /v1/nodes/:node_ip/instances==================================
    # 测试 ip 为 master 时  GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("Test get nodes instances response http code with master ip")
    re3 = m.get_nodes_instances(master_ip)
    assert_status_code(re3, 200)

    # 测试 ip 为 slave 时  GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("Test get nodes instances response http code with slave ip")
    re3 = m.get_nodes_instances(slave_ip)
    assert_status_code(re3, 200)

    # 测试 ip 不存在时 GET /v1/nodes/:node_ip/instances 返回的http_code
    Logger.log_info("Test get nodes instances response http code with invalid ip")
    re3 = m.get_nodes_instances("192.168.1.1")
    assert_status_code(re3, 404)