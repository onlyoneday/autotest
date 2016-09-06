import json
from  Logger import Logger

def json_compare(re_data,jsonfile,api_name):
    j = json.load(open(jsonfile))
    fail_flag = 0
    for i in j:
        if i["api"] == api_name:
            data = i["response"]["data"]
            for key in data:
                if re_data.get(key,None) == None:
                    msg_fail = key + "isn't in response of "+ i["api"]
                    Logger.log_fail(msg_fail)
                    fail_flag = 1
    if fail_flag == 0:
        msg_pass = api_name + " response json is correct."
        Logger.log_pass(msg_pass)

#if __name__ == '__main__':