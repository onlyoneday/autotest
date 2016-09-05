from  auth_api import authapi
from  node_api import nodeapi

import requests
import json

test = authapi()

# valid login
token = test.login('admin@dataman-inc.com' , 'Dataman1234' , 200)
# invalid login
test.login('admin@dataman-inc.com' , 'Dataman1234ttt' , 400)
