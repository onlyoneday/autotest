import requests
import json

url = "http://192.168.1.155:9999"


class swarmapi(object):

    def __init__(self):
        pass


    #登录
    def login(self,email ,password):
        payload = {"email": email ,"password": password}
        re = requests.post(url + "/v1/login" ,data=json.dumps(payload))
        if re.status_code ==400:
            return re.status_code ,re.json()
        if re.status_code ==401:
            return re.status_code ,re.json()
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    #退出登录
    def logout(self,token):
        re = requests.post(url + "/v1/logout" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    #修改密码
    def get_all_userinfo(self,token):
        re = requests.get(url + "/account/v1/accounts" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    #根据用户id获取用户信息
    def get_userinfo_byid(self,token,id):
        re = requests.get(url + "/account/v1/accounts/"+str(id)+"/groups" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    #根据用户id获取所属组
    def get_groupinfo_byuserid(self,token,id):
        re = requests.get(url + "/account/v1/accounts/"+str(id) ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()




    # curl -XGET localhost:5013/account/v1/accounts/1/groups

    #curl -XGET localhost:5013/account/v1/accounts/1




    def getuserinfo(self,token):
        re = requests.get(url + "/account/v1/aboutme" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

    def getgroupinfo(self,token):
        re = requests.get(url + "/account/v1/groups" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

