'''
Created on 2017.5.16
<TXT file> have samplesID
@author: Dahye.Lee
'''

# -*- coding: utf-8 -*-

import httplib
import json
import sys

url = raw_input("Enter the url: ")
userid = sys.argv[1]
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
print samples

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
