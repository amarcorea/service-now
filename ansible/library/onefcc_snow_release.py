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


def info_release(release_number, **module_args):
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
        response = {"mensaje": "ERROR, no se pudo crear la release: " + str(e)}
        #log("ERROR, no se pudo crear la release: " + str(e))

    return response


def validateOptions(module):

    if module.params["state"] == "info_release":
        return info_release(module.params["release"],**module.params)


def run_module():
    # define available arguments/parameters a user can pass to the module

    module_args = {
        "state": {
            "default": "present",
            "choices": ["present", "to_certification", "approve", "to_preprod", "info_release"]
        },
        "sn_user": {"required": False, "type": "str"},
        "sn_pass": {"required": False, "type": "str", "no_log": True},
        "sn_base": {"required": True, "type": "str"},
        "sn_uri": {"required": False, "type": "str", "default": "/api/now/v2/table/rm_release"},
        "timeout": {"required": False, "type": "int", "default": 300},
        "release": {"required": False, "type": "str"}
        # "data": {"required": True, "type": "dict", "default": None},
        # "authType": {"required": False, "type": "str", "default": "Basic"},
        # "params": {"required": False, "type": "dict", "default": None},
        # "headers": {"required": False, "type": "dict", "default": None},


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
    if response.status_code == 200:

        #TODO Validar respuesta para regresar elemento
        if len(response.json()['result']) > 0:
            result['message'] = response.json()["result"][0]
            result['changed'] = True
        else:
            result['message'] = "La release "+module.params["release"]+" no existe en "+module.params["sn_base"]
            result['changed'] = False
            
        module.exit_json(**result)

    else:
        module.fail_json(msg="Error en la respuesta", **result)


def main():
    run_module()


def standalone():
    module_args=dict(
        state="info_release",
        sn_user="user_sgt_pipeline_rlse",
        sn_pass="user_sgt_pipeline_rlse#Test1",
        sn_base="https://santandertest.service-now.com",
        sn_uri="/api/now/v2/table/rm_release",
        release="RLSE05951001",
        timeout=30
    )
    
    response = info_release(module_args["release"],**module_args)

    response_item = json.loads(response.text)
    print("Code: "+str(response.status_code))
    print("Len : "+str(len(response.json()['result'])))

if __name__ == '__main__':
    main()
    #standalone()
