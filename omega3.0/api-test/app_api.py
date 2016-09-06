import configparser
import requests
from  Logger import Logger
import json

cf = configparser.ConfigParser()
cf.read("test.conf")
url = cf.get("all", "url")


class appapi(object):

    def __init__(self):
        pass


    #1获取应用列表
    def getapplist(self,token,expectcode):
        re = requests.get(url + "/v1/apps" ,headers={'Authorization': token})
        #print(re.text)
        apicase = 'get app list'
        if expectcode ==200 and re.status_code == expectcode :
            Logger.log_info("valid  " + apicase)
            if re.json()["data"]['apps'][0]['id'] != None  and int(re.json()["code"])==0 :
                Logger.log_pass("valid " + apicase + " passed")
            else:
                Logger.log_fail("valid " + apicase + " failed")
        elif expectcode ==401 and re.status_code == expectcode:
            Logger.log_info("invalid " + apicase)
            if int(re.json()["code"])==1 :
                Logger.log_pass("invalid " + apicase + " passed")
            else:
                Logger.log_fail("invalid "+apicase+" test failed return code is "+str(re.json()["code"])+"but it must be 1")
        else:
            Logger.log_fail(apicase+" uncatched error " + str(re.status_code))
