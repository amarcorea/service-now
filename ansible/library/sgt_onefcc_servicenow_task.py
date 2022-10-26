#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import requests
import json
from datetime import datetime

#__metaclass__ = type

def log(message):
    print(str(datetime.now()) + ": " + message)

def update_task(**release):

    response = None
    endpoint = release["sn_base"] + \
        release["sn_uri"] + "/" + release["data"]["id"]

    try:
        if release["authType"].lower() == "basic":
            response = requests.put(
                url=endpoint,
                headers=release["headers"],
                auth=(release["sn_user"], release["sn_pass"]),
                data=release["data"],
                params=release["params"],
                timeout=release["timeout"]
            )
        else:
            response = requests.put(
                url=endpoint,
                headers=release["headers"],
                data=release["data"],
                params=release["params"],
                timeout=release["timeout"]
            )

    except Exception as e:
        response = {
            "mensaje": "ERROR, no se pudo actualizar la task: " + str(e)}
        log("ERROR, no se pudo actualizar la task: " + str(e))

    return response

def create_task(**release):

    response = None
    endpoint = release["sn_base"] + release["sn_uri"]

    try:
        if release["authType"].lower() == "basic":
            response = requests.post(
                url=endpoint,
                headers=release["headers"],
                auth=(release["sn_user"], release["sn_pass"]),
                data=release["data"],
                params=release["params"],
                timeout=release["timeout"]
            )
        else:
            response = requests.post(
                url=endpoint,
                headers=release["headers"],
                data=release["data"],
                params=release["params"],
                timeout=release["timeout"]
            )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo crear la task: " + str(e)}
        log("ERROR, no se pudo crear la task: " + str(e))

    return response

def validateOptions(module):
    
     # if module.params["state"] == "absent" or module.params["state"] == "cancel":
    #    return
    #
    
    #
    # if module.params["state"] == "approve":
    #    return

    if module.params["state"] == "present" or module.params["state"] == "create":
        return create_task(**module.params)

    if module.params["state"] == "update":
        return update_task(**module.params)

def main():

    args_modules = {
        "state": {
            "default": "present",
            "choices": ["present", "absent", "update", "approve", "create", "delete"]
        },
        "sn_user": {"required": False, "type": "str", "default": ""},
        "sn_pass": {"required": False, "type": "str", "default": "", "no_log": True},
        "sn_base": {"required": True, "type": "str"},
        "sn_uri": {"required": False, "type": "str", "default": "/api/now/v2/table/rm_task"},
        "data": {"required": True, "type": "dict", "default": None},
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
        "email": "acr2amrhp1dd@random.local",
        "status": "active",
        "id": "6224"
    }

    headers = {'Authorization': "Bearer {}".format(token)}

    release_params = {
        "sn_base": "https://gorest.co.in",
        "sn_uri": "/public/v2/users",
        "sn_user": "",
        "sn_pass": "",
        "data": data,
        "headers": headers,
        "authType": "token"
    }

    #query = { 'sysparm_fields': 'sys_id,number' }

    # return create_release(**release_params)
    return update_release(**release_params)

if __name__ == '__main__':
    main()
