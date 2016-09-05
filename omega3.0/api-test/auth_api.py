import requests
import json
import configparser
from  Logger import Logger

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")

class authapi(object):

    def __init__(self):
        pass


    #1登录
    def login(self, email, password, expectcode):
        payload = {"email": email ,"password": password}
        re = requests.post(url + "/v1/login" ,data=json.dumps(payload))
        apicase='login'
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("valid  "+apicase)
            if len(re.json()["data"])==32 and int(re.json()["code"])==0 :
                Logger.log_high("valid "+apicase+" passed")
                return re.json()['data']
            else:
                Logger.log_fail("valid "+apicase+" failed")
        elif expectcode ==400 and re.status_code == expectcode:
            Logger.log_normal("invalid "+apicase )
            if int(re.json()["code"])==12007 :
                Logger.log_high("invalid "+apicase+" passed")
            else:
                Logger.log_fail("invalid "+apicase+" failed return code is "+int(re.json()["code"])+"but it must be 12007")
        else:
            Logger.log_fail(apicase+" uncatched error " + str(re.status_code))




    #2退出登录
    def logout(self,token,expectcode):
        re = requests.post(url + "/v1/logout" ,headers={'Authorization': token})
        apicase = 'logout'
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("valid  " + apicase)
            if re.json()["data"]=='success' and int(re.json()["code"])==0 :
                Logger.log_high("valid " + apicase + " passed")
            else:
                Logger.log_fail("valid " + apicase + " failed")
        elif expectcode ==401 and re.status_code == expectcode:
            Logger.log_normal("invalid " + apicase)
            if int(re.json()["code"])==1 :
                Logger.log_high("invalid " + apicase + " passed")
            else:
                Logger.log_fail("invalid "+apicase+" test failed return code is "+int(re.json()["code"])+"but it must be 1")
        else:
            Logger.log_fail(apicase+" uncatched error " + str(re.status_code))

    #3修改密码
    def change_passwd(self,token):
        re = requests.put(url + "/v1/password" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    # 4获取当前用户信息
    def getuserinfo(self, token,expectcode):
        re = requests.get(url + "/v1/aboutme", headers={'Authorization': token})
        apicase = 'get user info'
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("valid  " + apicase)
            if re.json()["data"]['email'] != None and int(re.json()["code"])==0 :
                Logger.log_high("valid " + apicase + " passed")
            else:
                Logger.log_fail("valid " + apicase + " failed")
        elif expectcode ==401 and re.status_code == expectcode:
            Logger.log_normal("invalid " + apicase)
            if int(re.json()["code"])==1 :
                Logger.log_high("invalid " + apicase + " passed")
            else:
                Logger.log_fail("invalid "+apicase+" test failed return code is "+int(re.json()["code"])+"but it must be 1")
        else:
            Logger.log_fail(apicase+" uncatched error " + str(re.status_code))


    #5获取所有用户
    def get_all_user_info(self,token,expectcode):
        re = requests.get(url + "/v1/accounts" ,headers={'Authorization': token})
        apicase = 'get all user info'
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("valid  " + apicase)
            if  int(re.json()["code"])==0 :
                Logger.log_high("valid " + apicase + " passed")
            else:
                Logger.log_fail("valid " + apicase + " failed")
        elif expectcode ==401 and re.status_code == expectcode:
            Logger.log_normal("invalid " + apicase)
            if int(re.json()["code"])==1 :
                Logger.log_high("invalid " + apicase + " passed")
            else:
                Logger.log_fail("invalid " + apicase + " test failed return code is " + int(re.json()["code"]) + "but it must be 1")
        else:
            Logger.log_fail(apicase + "uncatched error " + str(re.status_code))

    #6创建用户 need docs




    #7根据用户id获取用户信息
    def get_groupinfo_byuserid(self,token,id,expectcode):
        re = requests.get(url + "/v1/accounts/"+str(id) ,headers={'Authorization': token})
        apicase = 'get group info  by userid'
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("valid  " + apicase)
            if  int(re.json()["code"])==0 :
                Logger.log_high("valid " + apicase + " passed")
            else:
                Logger.log_fail("valid " + apicase + " failed")
        elif expectcode ==401 and re.status_code == expectcode:
            Logger.log_normal("invalid " + apicase)
            if int(re.json()["code"])==1 :
                Logger.log_high("invalid " + apicase + " passed")
            else:
                Logger.log_fail("invalid " + apicase + " test failed return code is " + int(re.json()["code"]) + "but it must be 1")
        elif expectcode ==404 and re.status_code == expectcode:
            Logger.log_normal("invalid " + apicase)
            if int(re.json()["code"])==1 :
                Logger.log_high("invalid " + apicase + " passed")
            else:
                Logger.log_fail("ttest get group info by userid failed return code is "+int(re.json()["code"])+"but it must be 1")
        else:
            Logger.log_fail(apicase + "uncatched error " + str(re.status_code))
