from  auth_api import authapi
from  node_api import nodeapi
from  app_api import appapi

import configparser
import requests
import json

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")
user = cf.get("auth", "user")
passwd = cf.get("auth", "passwd")
wrong_user = cf.get("auth", "wrong_user")
wrong_passwd = cf.get("auth", "wrong_passwd")
wrong_token = cf.get("auth", "wrong_token")
wrong_nodeip = cf.get("node", "wrong_nodeip")

test = authapi()

def gettoken( email , password):
    payload = {"email": email , "password": password}
    re = requests.post(url + "/v1/login" , data=json.dumps(payload))
    return re.json()['data']


def getnodeip( token ):
    re = requests.get(url + "/v1/nodes" , headers={'Authorization': token})
    return re.json()['data']['masters'][0]['ip']

token=gettoken(user , passwd)



#POST /v1/login
# valid login
test.login(user , passwd , 200)
# invalid login
test.login(wrong_user , wrong_passwd , 400)
#

#POST /v1/logout
# valid logout
test.logout(gettoken(user , passwd) , 200)
# invalid logout
test.logout(wrong_token , 401)

#GET /v1/accounts/:account_id
# valid get group info  by userid
test.get_all_user_info(token , 200)
# invalid get_all_user_info
test.get_all_user_info(wrong_token , 401)

#GET /v1/accounts/:account_id
# valid get group info  by userid
test.get_groupinfo_byuserid(token , 1,200)
# invalid get group info  by userid
test.get_groupinfo_byuserid(wrong_token , 1,401)
test.get_groupinfo_byuserid(token , 999,404)

#GET /v1/accounts/:account_id
# valid get user info
test.getuserinfo(token , 200)
# invalid get user info
test.getuserinfo(wrong_token , 401)


#node
node = nodeapi()
nodeip = getnodeip(token)


#GET /v1/nodes/
# valid get node list
node.getnodelist(token , 200)
# invalid get node list
node.getnodelist(wrong_token , 401)

# GET  /v1/nodes/:node_ip/info
# valid get node info by ip
node.getnodeinfobyip(token , nodeip,200)
# invalid get node info by ip
node.getnodeinfobyip(wrong_token , nodeip,401)
# invalid get node info by ip
node.getnodeinfobyip(token , wrong_nodeip,404)


# app
app = appapi()

# GET /v1/apps
# invalid get app list
app.getapplist(token , 200)
# invalid get app list
app.getapplist(wrong_token , 401)