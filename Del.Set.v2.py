'''
Created on 2017.5.17
@author: Dahye.Lee
'''

# -*- coding: utf-8 -*-

import httplib
import json
import sys


def USAGE():
    print 'python', sys.argv[0], '<userID>'


def getToken(url, userid):
    params = json.dumps({"userid": userid})
    headers = {"Accept": "application/json", "Content-Type": "application/json;charset=UTF-8"}

    conn = httplib.HTTPConnection(url)
    conn.request("POST", "/TOKENS", params, headers)

    response = conn.getresponse()
    print '=======TOKEN========'
    print response.status, response.reason
    data = response.read()
    conn.close()

    token = {}
    token["x-cl-"+data[2:7]] = data[11:-2]

    return token


def getSetInfo(url, token, userid):
    params = json.dumps({"userid": userid})

    conn = httplib.HTTPConnection(url)
    conn.request("GET", "/USERS/"+userid+"/SETS", params, token)

    resp = conn.getresponse()
    print '=======STATUS======='
    print resp.status, resp.reason

    print '=============RESULT==============='
    data1 = resp.read()
    lLine = data1.split(',')

    for line in lLine:
        if line.startswith('"name'):
            if line.endswith('"'):
                print '----------------------------------'
                print '*Setname :', line[line.find(':"')+2:line.rfind('"')]
            else:
                pass

        elif line.startswith('"id'):
            if len(line[line.find(':"')+2:line.rfind('"')]) == 24:
                setid = line[line.find(':"')+2:line.rfind('"')]
                print ' Setid :', setid

                conn.close()
                getSetProfile(url, token, userid, setid)

    print '----------------------------------'


def getSetProfile(url, token, userid, setid):
    params = json.dumps({"userid": userid})
    conn = httplib.HTTPConnection(url)
    conn.request("GET", "/USERS/"+userid+"/SETS/"+setid+"/PROFILE?", params, token)
    resp = conn.getresponse()
    data2 = resp.read()

    for i in data2.split(',"names"'):
        if i.startswith('{"ids"'):
            sampleID = i[i.find(':')+1::]
            print ' SampleID :', sampleID

    conn.close()


def deleteSet(url, userid, token):
    setid = raw_input("Enter the setid: ")
    params = json.dumps({"userid": userid})

    conn = httplib.HTTPConnection(url)
    conn.request("DELETE", "/USERS/"+userid+"/SETS/"+setid, params, token)
    resp = conn.getresponse()

    print '========DELETE STATUS========'
    print resp.status, resp.reason

    conn.close()


def main():
    url = raw_input("Enter the url: ")

    userid = sys.argv[1]
    token = getToken(url, userid)
    getSetInfo(url, token, userid)

    while True:
        Q1 = raw_input("-> Would you like to delete the Set?(y/n) ")
        Q1 = Q1.lower()
        print '=========================================='

        if Q1 == 'y' or Q1 == 'yes':
            deleteSet(url, userid, token)
        else:
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        USAGE()
        sys.exit()
    main()
