import json
from  Logger import Logger

# def json_compare(re_data,jsonfile,api_name):
#     j = json.load(open(jsonfile))
#     fail_flag = 0
#     for i in j:
#         if i["api"] == api_name:
#             data = i["response"]["data"]
#             for key in data:
#                 if isinstance(key,dict):
#                     data2 = key
#                     for key2 in data2:
#                         try:
#                             re_data[0][key]
#                         except:
#                             msg_fail = key2 + " isn't in response of " + i["api"]
#                             Logger.log_fail(msg_fail)
#                             fail_flag = 1
#                     break
#                 else:
#                     try:
#                         re_data[key]
#                     except:
#                         msg_fail = key + " isn't in response of " + i["api"]
#                         Logger.log_fail(msg_fail)
#                         fail_flag = 1
#
#     if fail_flag == 0:
#         msg_pass = i["api"] + " response json is correct."
#         Logger.log_pass(msg_pass)

def json_compare(re_data,jsonfile,api_name):
    j = json.load(open(jsonfile))
    fail_flag = 0
    for i in j:
        if i["api"] == api_name:
            data = i["response"]["data"]
            #如果data是list
            if isinstance(data,list):
                data2 = data[0]
                re_data2 = re_data[0]
                for key in data2:
                    try:
                        get_key = re_data2[key]
                    except:
                        msg_fail = key + " isn't in response of " + i["api"]
                        Logger.log_fail(msg_fail)
                        fail_flag = 1
                    break
            #如果data是dict
            else:
                for key in data:
                    try:
                        get_key = re_data[key]
                    except:
                        msg_fail = key + " isn't in response of " + i["api"]
                        Logger.log_fail(msg_fail)
                        fail_flag = 1

    if fail_flag == 0:
        msg_pass = i["api"] + " response json is correct."
        Logger.log_pass(msg_pass)


if __name__ == '__main__':
    j = json.load(open("metrics.json"))
    for i in j:
        if i["api"] == "GET /v1/nodes/:node_ip/instances":
            re_data = i["response"]["data"]

    json_compare2(re_data, "metrics.json", "GET /v1/nodes/:node_ip/instances")
