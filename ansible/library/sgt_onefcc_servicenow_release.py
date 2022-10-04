#!/usr/bin/python

#from lib2to3.pgen2 import token
import sys
#from ansible.module_utils.basic import AnsibleModule
#from requests.adapters import HTTPAdapter
import requests
import json
#import os
#from os import path
from time import sleep
#import http.client
import ssl
#import chardet
#import mimetypes
#import sys
#import logging
#import http.client as http_client
#from logging import getLogger, INFO
#from concurrent_log_handler import ConcurrentRotatingFileHandler
from datetime import datetime
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#http_client.HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True



__metaclass__ = type

SGT_ONEFCC_BASE_RELEASE = "https://santandertest.service-now.com"
#SGT_ONEFCC_URI_RELEASE = '/api/now/v2/table/rm_release'
SGT_ONEFCC_URI_RELEASE = '/public/v2/users'
SGT_ONEFCC_LOG = True
#SGT_ONEFCC_LOG_HANDLER = None
#SGT_ONEFCC_LOG_ID = None

# def log(message):
#
#    global SGT_ONEFCC_LOG
#    global SGT_ONEFCC_LOG_HANDLER
#    global SGT_ONEFCC_LOG_ID
#
#    if SGT_ONEFCC_LOG:
#        try:
#            SGT_ONEFCC_LOG_HANDLER.info( SGT_ONEFCC_LOG_ID + ": " + str(datetime.now()) + ": " + message )
#        except Exception as e:
#            pass


def log(message):
    if SGT_ONEFCC_LOG:
        print(str(datetime.now()) + ": " + message)

def create_releasev2(**release):
    #servicenow_adapter = HTTPAdapter(max_retries=retries)
    #session = requests.Session()

    response = None
    
    release["sn_base"] = SGT_ONEFCC_BASE_RELEASE if "sn_base" not in release else release["sn_base"]
    release["sn_uri"] = SGT_ONEFCC_URI_RELEASE if "sn_user" not in release else release["sn_uri"]
    release["sn_user"] = "" if "sn_user" not in release else release["sn_user"]
    release["sn_pass"] = "" if "sn_pass" not in release else release["sn_pass"]
    release["data"] = None if "data" not in release else release["data"]
    release["headers"] = None if "headers" not in release else release["headers"]
    release["params"] = None if "params" not in release else release["params"]
    release["authType"] = "Basic" if "authType" not in release else release["authType"]
    release["timeout"] = 300 if "timeout" not in release else release["timeout"]

    endpoint = release["sn_base"] + release["sn_uri"]

    print(release)

    try:
        if release["authType"].lower() == "basic":
            response = requests.post(url=endpoint, headers=release["headers"], auth=(
                release["sn_user"], release["sn_pass"]), data=release["data"], params=release["params"], timeout=release["timeout"])
        else:
            response = requests.post(url=endpoint, headers=release["headers"], data=release["data"], params=release["params"], timeout=release["timeout"])

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo crear la release: " + str(e) }
        log("ERROR, no se pudo crear la release: " + str(e))

    return response

def create_release(sn_user, sn_pass, sn_instance, data, uri="/api/now/v2/table/rm_release", retries=3, authType="basic", params=None, headers=None, timeout=300):

    #servicenow_adapter = HTTPAdapter(max_retries=retries)
    #session = requests.Session()

    response = None
    endpoint = sn_instance + uri

    #query = { 'sysparm_fields': 'sys_id,number' }

    try:
        if authType.lower() == "basic":
            response = requests.post(endpoint, headers=headers, auth=(
                sn_user, sn_pass), data=str(data), params=params, timeout=timeout)
        else:
            print(str(data))
            response = requests.post(url=endpoint, headers=headers, data=data)

    except Exception as e:
        log("ERROR, no se pudo crear la release: " + str(e))

    return response


def validateOptions(module):

    #global SGT_ONEFCC_LOG
    #global SGT_ONEFCC_LOG_HANDLER
    #global SGT_ONEFCC_LOG_ID

    if module.params["log"]:
        SGT_ONEFCC_LOG = True
        # try:
        #SGT_ONEFCC_LOG_HANDLER = getLogger(__name__)
        #logfile = os.path.abspath(module.params["/onefcc_dev/marcorea/log.log"])
        #rotateHandler = ConcurrentRotatingFileHandler(logfile, "a", 100*1024*1024, 3)
        # SGT_ONEFCC_LOG_HANDLER.addHandler(rotateHandler)
        # SGT_ONEFCC_LOG_HANDLER.setLevel(INFO)
        #SGT_ONEFCC_LOG = True
        #SGT_ONEFCC_LOG_ID = "log.log"
        # except Exception as e:
        #    log("ERROR, no se pudo crear el logfile: " + str(e) )
        #    SGT_ONEFCC_LOG = False

    if module.params["state"] == "present" or module.params["state"] == "create":
        return create_release(
            module.params["usuario"],
            module.params["password"],
            module.params["instancia_sn"],
            module.params["data"],
            module.params["uri"],
            module.params["retries"],
            module.params["authType"],
            module.params["params"],
            module.params["headers"],
            module.params["timeout"]
        )

    # if module.params["state"] == "absent" or module.params["state"] == "cancel":
    #    return
    #
    # if module.params["state"] == "update":
    #    return
    #
    # if module.params["state"] == "approve":
    #    return


def main():

    args_modules = {
        "state": {
            "default": "present",
            "choices": ["present", "absent", "update", "approve", "create", "delete"]
        },
        "usuario": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "instancia_sn": {"required": True, "type": "str"},
        "data": {"required": True, "type": "dict"},
        "uri": {"required": False, "type": "str", "default": "/api/now/v2/table/rm_release"},
        "log": {"required": False, "type": "bool", "default": False},
        "retries": {"required": False, "type": "int", "default": 3},
        "authType": {"required": False, "type": "str", "default": "Basic"},
        "params": {"required": False, "type": "dict", "default": None},
        "headers": {"required": False, "type": "dict", "default": None},
        "timeout": {"required": False, "type": "int", "default": 300},

    }

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    module = AnsibleModule(
        argument_spec=args_modules,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json(**result)
    else:
        response = validateOptions(module)

    result["message"] = json.loads(response.text)

    if response.status_code <= 204:
        result["message"] = response.json()
        result["changed"] = True
        module.exit_json(**result)
    else:
        module.fail_json(msg="Error en la respuesta!", **result)


def local():
    token = "d48cf0a45d36311ab405e1fd4cd1b533da3b2f22b5dceb30c48b8f6151eb3bec"
    data = {
        "name": "Foo Jhonson",
        "gender": "male",
        "email": "foo.jhonson@local.email",
        "status": "active"
        }

    headers = {'Authorization': "Bearer {}".format(token)}

    
    #query = { 'sysparm_fields': 'sys_id,number' }
    query = None

    return create_release("", "", "https://gorest.co.in", data, "/public/v2/users", 3, "token", query, headers, 300)

def localv2():
    token = "d48cf0a45d36311ab405e1fd4cd1b533da3b2f22b5dceb30c48b8f6151eb3bec"
    data = {
        "name": "Foo Jhonson",
        "gender": "male",
        "email": "foo.jhonson@localv2.email",
        "status": "active"
        }

    headers = {'Authorization': "Bearer {}".format(token)}

    release_params = {
        "sn_base": "https://gorest.co.in",
        "sn_uri": "/public/v2/users",
        "sn_user": "",
        "sn_pass": "",
        "data": data,
        "headers": headers,
        "authType": "TOKEN"
    }
    
    #query = { 'sysparm_fields': 'sys_id,number' }
    

    return create_releasev2(**release_params)

if __name__ == '__main__':
    if sys.argv[1] == "local":
        print("En modo local")
        respuesta = localv2()
        print(respuesta.json())
        # local()
    else:
        print("En modo ansible")
        # main()
