from selenium import webdriver
import time
# from threading import Thread
import sys
import multiprocessing
from multiprocessing import Pool

login_url = "http://192.168.1.118:81/ui/auth/login"

email = "admin"
password = "dataman1234"


#====================================================================================
def login(no):
    # driver = webdriver.PhantomJS()
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(login_url)

    driver.find_element_by_name("userName").send_keys(email)
    driver.find_element_by_name("Password").send_keys(password)
    driver.find_element_by_id("login-btn-login").click()

    #--------------------------
    start_login = time.time()
    try:
        driver.find_element_by_css_selector("#index-to-stack>span")
    except Exception as e:
        print(e)
    finally:
        end_login = time.time()
    #--------------------------
    driver.quit()

    time_length = end_login - start_login
    # print("login user %d, takes %s seconds" % (no, time_length))
    print("%s" % time_length)

#====================================================================================
def app_list(no):
    # driver = webdriver.PhantomJS()
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(login_url)


    driver.find_element_by_name("userName").send_keys(email)
    driver.find_element_by_name("Password").send_keys(password)
    driver.find_element_by_id("login-btn-login").click()

    time.sleep(no*1.5)

    try:
        driver.find_element_by_id("index-to-node").click()
    except Exception as e:
        print(e)
    # finally:
        # print("1")


    try:
        driver.find_element_by_id("master-leader")
    except Exception as e:
        print(e)
    # finally:
        # print("2")

    time.sleep(no*1.5)
    #--------------------------
    try:
        driver.find_element_by_id("index-to-stack").click()
    except Exception as e:
        print(e)
    finally:
        start_login = time.time()
        # print("3")

    try:
        driver.find_element_by_id("stackListSuspended0")
    except Exception as e:
        print(e)
    finally:
        end_login = time.time()
        # print("4")
    #--------------------------

    driver.quit()
    time_length = end_login - start_login

    print("%s" % time_length)

#====================================================================================
# def app_list(no):
#     # driver = webdriver.PhantomJS()
#     driver = webdriver.Firefox()
#     driver.get(login_url)
#
#
#     driver.find_element_by_name("Email").send_keys(email)
#     driver.find_element_by_name("Password").send_keys(password)
#     driver.find_element_by_id("login-btn-login").click()
#
#     for i in range(1,1000):
#         try:
#             driver.find_element_by_id("index-to-node").click()
#         except Exception:
#             time.sleep(0.05)
#         else:
#             break
#
#     for i in range(1, 10000):
#         try:
#             driver.find_element_by_xpath("//table/tbody/tr[1]/td[1]")
#         except Exception:
#             time.sleep(0.1)
#         else:
#             break
#     #--------------------------
#     for i in range(1, 10000):
#         try:
#             driver.find_element_by_id("index-to-stack").click()
#         except Exception:
#             time.sleep(0.1)
#         else:
#             start_login = time.time()
#             break
#
#     for i in range(1, 1000):
#         try:
#             # print("wait utill app list apear %d" % i)
#             driver.find_element_by_id("stackListSuspended0")
#         except Exception:
#             time.sleep(0.1)
#         else:
#             end_login = time.time()
#             break
#     #--------------------------
#
#     driver.quit()
#     time_length = end_login - start_login
#     # print("apps_list user %d, takes %s seconds" % (no,time_length))
#
#     print("%s" % time_length)

#====================================================================================
# def cluster_info(no):
#     # driver = webdriver.PhantomJS()
#     driver = webdriver.Firefox()
#     driver.get(login_url)
#
#     driver.find_element_by_name("Email").send_keys(email)
#     driver.find_element_by_name("Password").send_keys(password)
#     driver.find_element_by_id("login-btn-login").click()
#
#     time.sleep(no*1.5)
#     # --------------------------
#
#     try:
#         driver.find_element_by_id("index-to-node").click()
#     except Exception:
#         time.sleep(0.1)
#     finally:
#         start_login = time.time()
#
#     # time.sleep(5)
#     try:
#         driver.find_element_by_id("master-leader")
#     except Exception:
#         time.sleep(0.01)
#     finally:
#         end_login = time.time()
#
#     # --------------------------
#
#     driver.quit()
#
#     time_length = end_login - start_login
#     # print("cluster_info user %d, takes %s seconds" % (no, time_length))
#
#     print("%s" % time_length)

#====================================================================================
def cluster_info(no):
    driver = webdriver.PhantomJS()
    # driver = webdriver.Firefox()
    driver.get(login_url)

    driver.find_element_by_name("Email").send_keys(email)
    driver.find_element_by_name("Password").send_keys(password)
    driver.find_element_by_id("login-btn-login").click()

    # --------------------------
    for i in range(1, 1000):
        try:
            driver.find_element_by_id("index-to-node").click()
        except Exception:
            time.sleep(0.1)
        else:
            start_login = time.time()
            break

    for j in range(1, 1000):
        try:
            driver.find_element_by_id("master-leader")
        except Exception:
            time.sleep(0.02)
        else:
            end_login = time.time()
            break
    # --------------------------

    driver.quit()

    time_length = end_login - start_login
    # print("cluster_info user %d, takes %s seconds" % (no, time_length))

    print("%s" % time_length)





if __name__ == '__main__':

    type = sys.argv[1]
    user = sys.argv[2]
    repeat = sys.argv[3]


    # ====================
    if type == "login":
        for i in range(1, int(repeat)+1):
            po = Pool()
            for i in range(1, int(user)+1):
                try:
                    po.apply_async(login, args=(int(user),))
                    # p = multiprocessing.Process(target=login, args=(i,))
                    # p.start()
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    # ====================
    elif type == "app_list":
        for i in range(1, int(repeat)+1):
            po = Pool()
            for i in range(1, int(user)+1):
                try:
                    po.apply_async(app_list, args=(int(user),))
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    # ====================
    elif type == "cluster_info":
        for i in range(1, int(repeat) + 1):
            # print("start")
            po = Pool()
            for i in range(1, int(user) + 1):
                try:
                    po.apply_async(cluster_info, args=(int(user),))
                except Exception as errtxt:
                    print(errtxt)
            po.close()
            po.join()

    else:
        print("Usage: main.py login|app_list|cluster_info n(users number) n(repeat number)")

