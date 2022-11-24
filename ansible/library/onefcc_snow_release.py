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

#ALLOW_CLOSE_CODES = ("Successful", "Successful automatic", "Successful with issues", "Unsuccessful", "Cancelled", "Rejected")

def log(message):
    print(str(datetime.now()) + ": " + message)

def info(release_number, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] 
    params={"sysparm_query": "number="+str(release_number) }

    try:
        response = requests.get(
            url=endpoint,
            auth=(module_args["sn_user"], module_args["sn_pass"]),
            params=params,
            timeout=module_args["timeout"]
        )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo obtener información de la release "+str(release_number)+": " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def info_approver(release_number, approver_name, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] 
    params={
        "sysparm_query": "sysapproval.number="+str(release_number)+"^approver.user_name="+str(approver_name),
        "sysparm_fields": "sys_id,state"
    }

    try:
        response = requests.get(
            url=endpoint,
            auth=(module_args["sn_user"], module_args["sn_pass"]),
            params=params,
            timeout=module_args["timeout"]
        )

    except Exception as e:
        response = {"mensaje": "ERROR, no se pudo obtener información del approver "+str(approver_name)+" de la release "+str(release_number)+": " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def create(**module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] 
    data={
        "parent":                           module_args["parent"],
        "u_requested_group":                module_args["group"],
        "u_reason":                         module_args["reason"],
        "u_risk":                           module_args["risk"],
        "short_description":                module_args["short_description"],
        "description":                      module_args["description"],
        "u_justification":                  module_args["justification"],
        "u_implementation_plan":            module_args["implementation_plan"],
        "u_preproduction_proposed_date":    module_args["preproduction_proposed_date"],
        "u_start_date":                     module_args["start_date"],
        "u_end_date":                       module_args["end_date"],
        "u_backout_plan":                   module_args["backout_plan"],
        "u_risk_and_impact_analysis":       module_args["risk_and_impact"],
        "u_test_plan":                      module_args["test_plan"]
        
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
        response = {"mensaje": "ERROR, no se pudo crear la release " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response

def to_certification(release_number, release_id, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] + "/" + release_id
    data={
        "state": module_args["status"]
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
        response = {"mensaje": "ERROR, no se pudo actualizar la release "+str(release_number)+": " + str(e)}

    return response

def to_waiting(release_number, release_id, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] + "/" + release_id
    data={
        "state": module_args["status"]
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
        response = {"mensaje": "ERROR, no se pudo cerrar la task "+str(release_number)+": " + str(e)}

    return response

def to_testing(release_number, release_id, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] + "/" + release_id
    data={
        "state": module_args["status"]
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
        response = {"mensaje": "ERROR, no se pudo cerrar la task "+str(release_number)+": " + str(e)}

    return response

def approve(approve_id, **module_args):
    response = None
    endpoint = module_args["sn_base"] + module_args["sn_uri"] + "/" + approve_id
    data={
        "state": module_args["status"]
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
        response = {"mensaje": "ERROR, no se pudo cerrar la task "+str(release_number)+": " + str(e)}

    return response

def validateOptions(module):

    if module.params["state"] == "info":
        return info(module.params["release"], **module.params)
    
    if module.params["state"] == "present" or module.params["state"] == "create":
        return create(**module.params)

    if module.params["state"] == "to_certification":
        module.params["status"] = "Certification"
        response = info(module.params["release"], **module.params).json()
        release_id = ""
        
        if len(response["result"]) > 0:
            release_id = response["result"][0]["sys_id"]
        
        return to_waiting(module.params["release"], release_id,  **module.params)
    
    if module.params["state"] == "to_waiting":
        module.params["status"] = "Waiting Accept"
        response = info(module.params["release"], **module.params).json()
        release_id = ""
        
        if len(response["result"]) > 0:
            release_id = response["result"][0]["sys_id"]
        
        return to_certification(module.params["release"], release_id,  **module.params)
    
    if module.params["state"] == "to_testing":
        module.params["status"] = "Testing"
        response = info(module.params["release"], **module.params).json()
        release_id = ""
        
        if len(response["result"]) > 0:
            release_id = response["result"][0]["sys_id"]
        
        return to_certification(module.params["release"], release_id,  **module.params)

    if module.params["state"] == "approve":
        module.params["status"] = "approved"
        module.params["sn_uri"] = "/api/now/v2/table/sysapproval_approver"
        response = info_approver(module.params["release"], module.params["approver"], **module.params).json()
        approver_id = ""
        
        if len(response["result"]) > 0:
            approver_id = response["result"][0]["sys_id"]
            state = response["result"][0]["state"]
            
        
        return approve(approver_id, **module.params)

def run_module():
    
    module_args = {
        "state": {
            "default": "present",
            "choices": ["present", "create", "to_certification", "to_waiting","approve", "to_preprod", "to_testing", "info"]
        },
        "sn_user": {"required": False, "type": "str"},
        "sn_pass": {"required": False, "type": "str", "no_log": True},
        "sn_base": {"required": True, "type": "str"},
        "sn_uri": {"required": False, "type": "str", "default": "/api/now/v2/table/rm_release"},
        "timeout": {"required": False, "type": "int", "default": 300},
        
        #Para certification, waiting, approve, testing
        "release":{ "type": "str" },

        #Para creación
        "parent": {"type": "str"},
        "group":{ "type": "str" },
        "reason":{ "type": "str" },
        "risk":{ "type": "str", "default": "Low" },
        "short_description":{ "type": "str" },
        "description":{ "type": "str" },
        "justification": { "type": "str" },
        "implementation_plan": { "type": "str" },
        "preproduction_proposed_date": { "type": "str" },
        "start_date":{ "type": "str" },
        "end_date":{ "type": "str" },
        "backout_plan":{ "type": "str" },
        "risk_and_impact":{ "type": "str" },
        "test_plan":{ "type": "str" },
        "work_notes":{"type":"str"},
        
        #Para aprobar
        "approver": {"type":"str"},

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
            ('state', 'info', ('release', 'sn_user', 'sn_pass','sn_base'), False),
        ],
        required_together=[
            ('sn_user', 'sn_pass','sn_base'),
        ],
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
                result['message'] = "La release "+module.params["release"]+" no existe!"
                result['changed'] = False
        #Aplica para otras acciones
        else:
            if "number" in response.json()["result"] or "sys_id" in response.json()["result"]:
                result['message'] = response.json()["result"]
                result['changed'] = True
            else:
                result['message'] = "No se pudo obtener la info de la release: "+module.params["release"]
                result['changed'] = False
                module.fail_json(msg="Error general en la respuesta", **result)
            
        module.exit_json(**result)

    else:
        module.fail_json(msg="Error general en la respuesta", **result)


def main():
    run_module()

if __name__ == '__main__':
    main()