#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
import requests
import json
from datetime import datetime


###DOCUMENTATION = r'''
###---
###module: onefcc_snow_task
###
###short_description: Modulo de Tasks para ONEFCC Service Now
###
###version_added: "1.0.0"
###
###description: Modulo para crear, cerrar y obtener informacion acerca de las tasks.
###
###options:
###    state:
###        description: Es para indicar la opcion a realizar dentro de la task
###            - info_task. Para obtener informacion a cerca de la task
###            - incomplete.
###        required: false
###        type: bool
###    task:
###        description: Numero de la tarea a buscar, requerido si info_task esta presente
###        required: true
###        type: str
###    
###
#### Specify this value according to your collection
#### in format of namespace.collection.doc_fragment_name
###extends_documentation_fragment:
###    - my_namespace.my_collection.my_doc_fragment_name
###
###author:
###    - Marco Rea (@x25241)
###'''
###
###EXAMPLES = r'''
#### Pass in a message
###- name: Test with a message
###  my_namespace.my_collection.my_test:
###    name: hello world
###
#### pass in a message and have changed true
###- name: Test with a message and changed output
###  my_namespace.my_collection.my_test:
###    name: hello world
###    new: true
###
#### fail the module
###- name: Test failure of the module
###  my_namespace.my_collection.my_test:
###    name: fail me
###'''
###
###RETURN = r'''
#### These are examples of possible return values, and in general should use other names for return values.
###original_message:
###    description: The original name param that was passed in.
###    type: str
###    returned: always
###    sample: 'hello world'
###message:
###    description: The output message that the test module generates.
###    type: str
###    returned: always
###    sample: 'goodbye'
###'''

ALLOW_CLOSE_CODES = ("Successful", "Successful automatic", "Successful with issues", "Unsuccessful", "Cancelled", "Rejected")

def log(message):
    print(str(datetime.now()) + ": " + message)


def info(task_number, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] 
    params={"sysparm_query": "number="+str(task_number) }

    try:
        response = requests.get(
            url=endpoint,
            auth=(module_args["sn_user"], module_args["sn_pass"]),
            params=params,
            timeout=module_args["timeout"]
        )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo obtener información de la task "+str(task_number)+": " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def create(release_number, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] 
    data={
        "top_task":             release_number,
        "u_release":            release_number,
        "start_date":           module_args["start_date"],
        "end_date":             module_args["end_date"],
        "short_description":    module_args["short_description"],
        "description":          module_args["description"],
        "u_state_to_resolve":   module_args["state_resolve"],
        "type":                 module_args["type"],
        "assignment_group":     module_args["group"],
        "order":                module_args["order"],
        "u_technology":         module_args["technology"],
        "u_version":            module_args["version"],
        "u_application":        module_args["application"]
    }

    try:
        response = requests.post(
            url=endpoint,
            auth=(module_args["sn_user"], module_args["sn_pass"]),
            #params=params,
            data=json.dumps(data),
            timeout=module_args["timeout"]
        )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo crear la task en la release "+str(release_number)+": " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def update_inprogress(task_number, task_id, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] + "/" + task_id
    data={
        "state": module_args["status"],
        "assigned_to": module_args["assigned_to"]
    }

    if "work_notes" in module_args:
        data["work_notes"] = module_args["work_notes"]

    try:
        response = requests.put(
            url=endpoint,
            auth=(module_args["sn_user"], module_args["sn_pass"]),
            data=json.dumps(data),
            timeout=module_args["timeout"]
        )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo actualizar la task "+str(task_number)+": " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def update_closed(task_number, task_id, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] + "/" + task_id
    data={
        "state": module_args["status"],
        "u_close_code": module_args["close_code"],
        "close_notes": module_args["close_notes"],
        #"assigned_to": module_args["assigned_to"]
    }

    if "work_notes" in module_args:
        data["work_notes"] = module_args["work_notes"]

    try:
        response = requests.put(
            url=endpoint,
            auth=(module_args["sn_user"], module_args["sn_pass"]),
            data=json.dumps(data),
            timeout=module_args["timeout"]
        )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo cerrar la task "+str(task_number)+": " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def validateOptions(module):

    if module.params["state"] == "info":
        return info(module.params["task"], **module.params)
    
    if module.params["state"] == "present" or module.params["state"] == "create":
        return create(module.params["release"], **module.params)

    if module.params["state"] == "in_progress":
        module.params["status"] = "Work in Progress"
        response = info(module.params["task"], **module.params).json()
        task_id = ""
        
        if len(response["result"]) > 0:
            task_id = response["result"][0]["sys_id"]
        
        return update_inprogress(module.params["task"], task_id,  **module.params)
    
    if module.params["state"] == "closed":

        module.params["status"] = "Closed Complete"

        if module.params["close_code"] not in ALLOW_CLOSE_CODES:
            return {"result": {"mensaje":"El parámetro close_code no cumple con el catálogo!" } }

        response = info(module.params["task"], **module.params).json()
        task_id = ""
        
        if len(response["result"]) > 0:
            task_id = response["result"][0]["sys_id"]
        
        return update_closed(module.params["task"], task_id,  **module.params)

def run_module():
    
    module_args = {
        "state": {
            "default": "present",
            "choices": ["present", "create", "closed", "in_progress", "skipped", "incomplete", "info"]
        },
        "sn_user": {"required": False, "type": "str"},
        "sn_pass": {"required": False, "type": "str", "no_log": True},
        "sn_base": {"required": True, "type": "str"},
        "sn_uri": {"required": False, "type": "str", "default": "/api/now/v2/table/rm_task"},
        "timeout": {"required": False, "type": "int", "default": 300},

        #Para info, work in progress, complete task
        
        "task": {"type": "str"},
        #Para creación
        "release":{ "type": "str" },
        "start_date":{ "type": "str" },
        "end_date":{ "type": "str" },
        "short_description":{ "type": "str" },
        "description":{ "type": "str" },
        "state_resolve":{ "type": "str" },
        "type":{ "type": "str" },
        "group":{ "type": "str" },
        "order":{ "type": "str" },
        "application":{ "type": "str" },
        "technology":{ "type": "str" },
        "version":{ "type": "str" },
        
        #Para update, work in progress, complete task
        "assigned_to":{"type":"str"},
        "work_notes":{"type":"str"},
        "close_code":{"type":"str"},
        "close_notes":{"type":"str"}

    }

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        required_if=[
            ('state', 'info', ('task', 'sn_user', 'sn_pass','sn_base') ),
            ('state', 'present', ('release', 'start_date', 'end_date', 'short_description', 'state_resolve', 'type', 'application' ,'group', 'description', 'technology', 'sn_user', 'sn_pass','sn_base'), False),
        ]
    )

    if module.check_mode:
        module.exit_json(**result)
    else:
        response = validateOptions(module)

    result["message"] = json.loads(response.text)
    #result["message"] = json.loads(response.json())

    if response.status_code == 200 or response.status_code == 201:

        #Sólo consulta
        if module.params["state"] == "info":
            if len(response.json()['result']) > 0:
                result['message'] = response.json()["result"][0]
                result['changed'] = True
            else:
                result['message'] = "La task "+module.params["task"]+" no existe! en la release: "+module.params["release"]
                result['changed'] = False
        #Aplica para otras acciones
        else:
            if "number" in response.json()["result"]:
                result['message'] = response.json()["result"]
                result['changed'] = True
            else:
                result['message'] = "No se pudo obtener la info de la task desde la release: "+module.params["release"]
                result['changed'] = False
                module.fail_json(**result)
            
        module.exit_json(**result)

    else:
        module.fail_json(msg="Error general en la respuesta",**result)


def main():
    run_module()

if __name__ == '__main__':
    main()