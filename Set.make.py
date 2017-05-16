'''
Created on 2017.5.16
@author: Dahye.Lee
'''

# -*- coding: utf-8 -*-

import httplib
import json

url = "52.79.140.246:8080"
userid = raw_input("Enter the userid: ")
setfile = raw_input("Enter the SetFile Name: ")
setname = raw_input("Enter the Set Name: ")

params = json.dumps({"userid": userid})
headers = {"Accept": "application/json",
           "Content-Type": "application/json;charset=UTF-8"}

conn = httplib.HTTPConnection(url)
conn.request("POST", "/TOKENS", params, headers)

response = conn.getresponse()
print '==========TOKEN=============='
print response.status, response.reason
data = response.read()
conn.close()

samples = []
Infile = open(setfile, 'r')
lLine = Infile.readlines()

for line in lLine:
    samples.append(line.strip())

headers["x-cl-"+data[2:7]] = data[11:-2]
body = json.dumps({"name": setname, "samples": samples, "meta": {}})
headers["Content-Length"] = len(str(body))

conn = httplib.HTTPConnection(url)
conn.request("POST", "/USERS/"+userid+"/SETS", body, headers)
resp = conn.getresponse()

print '=======2nd Test STATUS======='
print resp.status, resp.reason

print '=========MSG================='
print resp.msg

print '=========BODY================'
data1 = resp.read()
print data1
conn.close()
