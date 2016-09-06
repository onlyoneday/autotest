from  auth_api import authapi
from  node_api import nodeapi

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


test = authapi()

def gettoken( email , password):
    payload = {"email": email , "password": password}
    re = requests.post(url + "/v1/login" , data=json.dumps(payload))
    return re.json()['data']

token=gettoken(user , passwd)



#POST /v1/login
# valid login
test.login(user , passwd , 200)
# invalid login
test.login(wrong_user , wrong_passwd , 400)


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