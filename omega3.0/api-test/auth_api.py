import requests
import json

url = "http://192.168.1.155:9999"


class swarmapi(object):

    def __init__(self):
        pass


    #1登录
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

    #2退出登录
    def logout(self,token):
        re = requests.post(url + "/v1/logout" ,headers={'Authorization': token})
        if re.status_code != 200:
            return re.status_code ,re.json()
        elif re.json()['code'] == 0:
            return re.status_code ,re.json()

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
