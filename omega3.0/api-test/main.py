from  api import swarmapi
import requests
import json

l = swarmapi()




token=l.login( 'admin@dataman-inc.com', 'Dataman1234' )[1]['data']


print(token)




# print(l.logout(token))




