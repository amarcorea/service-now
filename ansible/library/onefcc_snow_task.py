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


def validateOptions(module):

    if module.params["state"] == "info":
        return info(module.params["task"], **module.params)
    
    if module.params["state"] == "present" or module.params["state"] == "create":
        return create(module.params["release"], **module.params)


def run_module():
    # define available arguments/parameters a user can pass to the module

    module_args = {
        "state": {
            "default": "present",
            "choices": ["present", "create", "to_certification", "approve", "to_preprod", "info"]
        },
        "sn_user": {"required": False, "type": "str"},
        "sn_pass": {"required": False, "type": "str", "no_log": True},
        "sn_base": {"required": True, "type": "str"},
        "sn_uri": {"required": False, "type": "str", "default": "/api/now/v2/table/rm_task"},
        "timeout": {"required": False, "type": "int", "default": 300},
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
        "version":{ "type": "str" }

    }

    # module_args = dict(
    #    name=dict(type='str', required=True),
    #    new=dict(type='bool', required=False, default=False)
    # )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)
    else:
        response = validateOptions(module)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result["message"] = json.loads(response.text)
    if response.status_code == 200 or response.status_code == 201:

        #TODO Validar respuesta para regresar elemento
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
        module.fail_json(msg="Error en la respuesta", **result)


def main():
    run_module()


def standalone():
    module_args=dict(
        state="info",
        sn_user="user_sgt_pipeline_rlse",
        sn_pass="user_sgt_pipeline_rlse#Test1",
        sn_base="https://santandertest.service-now.com",
        sn_uri="/api/now/v2/table/rm_task",
        task="RTSK2253302",
        timeout=30
    )
    
    response = info(module_args["task"],**module_args)
    task = json.loads(response.text)
    
    print("Code: "+str(response.status_code))
    print("Len : "+str(len(response.json()['result'])))
    print("Len : "+str( "number" in response.json()["result"][0]))

if __name__ == '__main__':
    main()
    #standalone()
