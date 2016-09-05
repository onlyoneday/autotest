import requests
import json
from  Logger import Logger
url = "http://192.168.1.155:9999"


class authapi(object):

    def __init__(self):
        pass


    #1登录
    def login(self, email, password, expectcode):
        payload = {"email": email ,"password": password}
        re = requests.post(url + "/v1/login" ,data=json.dumps(payload))
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("test valid login ")
            if len(re.json()["data"])==32 and int(re.json()["code"])==0 :
                Logger.log_high("valid login test passed")
                return re.json()['data']
            else:
                Logger.log_fail("valid login test failed")
        elif expectcode ==400 and re.status_code == expectcode:
            Logger.log_normal("test invalid login ")
            if int(re.json()["code"])==12007 :
                Logger.log_high("invalid login test passed")
            else:
                Logger.log_fail("invalid login test failed return code is "+int(re.json()["code"])+"but it must be 12007")
        elif(re.status_code!=200 and re.status_code!=400):
            Logger.log_fail("uncatched error" + str(re.status_code))
        else:
            Logger.log_fail("uncatched error" + str(re.status_code))


    #2退出登录
    def logout(self,token,expectcode):
        re = requests.post(url + "/v1/logout" ,headers={'Authorization': token})
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_normal("test valid login ")
            if len(re.json()["data"])==32 and int(re.json()["code"])==0 :
                Logger.log_high("valid login test passed")
                return re.json()['data']
            else:
                Logger.log_fail("valid login test failed")
        elif expectcode ==400 and re.status_code == expectcode:
            Logger.log_normal("test invalid login ")
            if int(re.json()["code"])==12007 :
                Logger.log_high("invalid login test passed")
            else:
                Logger.log_fail("invalid login test failed return code is "+int(re.json()["code"])+"but it must be 12007")
        elif(re.status_code!=200 and re.status_code!=400):
            Logger.log_fail("uncatched error" + str(re.status_code))
        else:
            Logger.log_fail("uncatched error" + str(re.status_code))

    #3修改密码
    def change_passwd(self,token):
        re = requests.put(url + "/v1/password" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    # 4获取当前用户信息
    def getuserinfo(self, token):
        re = requests.get(url + "/v1/aboutme", headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code, re.json()
        elif re.json()['code'] == 0:
            return re.status_code, re.json()

    #5获取所有用户
    def get_all_user_info(self,token):
        re = requests.get(url + "/v1/accounts" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    #6创建用户 need docs




    #7根据用户id获取用户信息
    def get_groupinfo_byuserid(self,token,id):
        re = requests.get(url + "/v1/accounts/"+str(id) ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()
