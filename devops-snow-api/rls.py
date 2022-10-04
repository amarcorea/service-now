from config import USER, PASSWORD, INSTANCE
from config_release import ASSIGNMENT_GROUP, DESCRIPTION, IMPACT, IMPLEMENTATION_PLAN, JUSTIFICATION, PARENT, PLATFORM, REASON, REQUESTED_GROUP, RISK, SHORT_DESCRIPTION
from datetime import datetime, timedelta
from dict_text import rls_text
import pysnow

c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ''


def create_rls():
    # Define a resource, here we'll use the incident table API
    rls = c.resource(api_path='/table/rm_release')
    # Define Time date for rls management
    proposed_date = datetime.now()
    start_date = proposed_date + timedelta(minutes=30)
    end_date = proposed_date + timedelta(days=365)
    # Convert to string to parse Json
    proposed_date = proposed_date.strftime("%Y-%m-%d %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    # Set the payload
    new_record = {
        "parent": PARENT,
        "u_requested_group": REQUESTED_GROUP,
        "u_reason": REASON,
        "u_risk": RISK,
        "impact": IMPACT,
        "u_platform": PLATFORM,
        "short_description": SHORT_DESCRIPTION,
        "description": DESCRIPTION,
        "u_justification": JUSTIFICATION,
        "u_implementation_plan": IMPLEMENTATION_PLAN,
        "u_preproduction_proposed_date": proposed_date,
        "u_start_date": start_date,
        "u_end_date": end_date
    }
    # Create a new incident record
    result = rls.create(payload=new_record)
    for record in result.all():
        print(record['number'], rls_text[record['state']])
        sys_id_new = record['sys_id']
        state_new = record['state']
        rls_number_new = record['number']
        return sys_id_new, state_new, rls_number_new


def get_rls_status(rls=number):
    # Define a resource, here we'll use the release table API
    release = c.resource(api_path='/table/rm_release')
    
    response = release.get(query={'number': rls}, stream=True)

    # Iterate over the result and print out `sys_id` of the matching records.
    for record in response.all():
        print(record)
        print(record['number'], rls_text[record['state']])
        sys_id_local = record['sys_id']
        state_check = record['state']
        return sys_id_local, state_check


def update_rls_cert(rls=number):
    release = c.resource(api_path='/table/rm_release')

    update = {
        "state": "2",
        "work_notes": "Se pasa la Release a Certificacion"
    }
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "1":
        # Update 'short_description' and 'state' for 'INC012345'
        updated_record = release.update(query={'number': rls}, payload=update)
        # Print out the updated record
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_pre(rls=number):
    release = c.resource(api_path='/table/rm_release')

    update = {
        "state": "14",
        "work_notes": "Se pasa la Release a PRE"
    }
    rls_id, rls_state = get_rls_status(rls=rls)
    # Update 'short_description' and 'state' for 'INC012345'
    if rls_state == "2":
        # Update 'short_description' and 'state' for 'INC012345'
        updated_record = release.update(query={'number': rls}, payload=update)
        # Print out the updated record
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def approve_rls_pre(rls=number):
    approve_sys_id = ""
    release = c.resource(api_path='/table/sysapproval_approver')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "14":
        response = release.get(query={"approver.user_name": USER, "sysapproval.number": rls, 'sys_mod_count': '0'},
                               stream=True)
        for record in response.all():
            approve_sys_id = record['sys_id']
        update = {
            "state": "approved"
        }
        updated_record = release.update(query={'sys_id': approve_sys_id}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_test(rls=number):
    approve_sys_id = ""
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    open_task = get_open_task(rls=rls)
    if rls_state == "15" and len(open_task) == 0:
        update = {
            "state": "5",
            "work_notes": "Se pasa la Release a Pruebas"
        }
        updated_record = release.update(query={'number': rls}, payload=update)
        print(updated_record)
        rls_id, rls_state = get_rls_status(rls=rls)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_eval(rls=number):
    approve_sys_id = ""
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    open_task = get_open_task(rls=rls)
    if rls_state == "5" and len(open_task) == 0:
        update = {
            "state": "Assess",
        }
        updated_record = release.update(query={'number': rls}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def approve_rls_eval(rls=number):
    approve_sys_id = ""
    release = c.resource(api_path='/table/sysapproval_approver')
    rls_id, rls_state = get_rls_status(rls=rls)
    change = get_change_status(rls=rls)
    if rls_state == "6" or rls_state == "16":
        response = release.get(
            query={"approver.user_name": USER, "sysapproval": change, 'sys_mod_count': '0'},
            stream=True)
        for record in response.all():
            approve_sys_id = record['sys_id']
        update = {
            "state": "approved",
            "work_notes": "Se pasa la Release a Authorize"
        }
        updated_record = release.update(query={'sys_id': approve_sys_id}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_scheduled(rls=number):
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "8":
        update = {
            "state": "9",
            "work_notes": "Implementation"
        }
        updated_record = release.update(query={'number': rls}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_implement(rls=number):
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "9":
        update = {
            "state": "10",
            "work_notes": "Se pasa la Release a Revision",
            "u_close_code": "Successful automatic",
            "close_notes": "Desplegado en PRO"
        }
        updated_record = release.update(query={'number': rls}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_closed(rls=number):
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "10":
        update = {
            "state": "11",
            "work_notes": "Se pasa la Release a Revision",

        }
        updated_record = release.update(query={'number': rls}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_cancel_rls_new(rls=number):
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    open_task = get_open_task(rls=rls)
    update = {
        "state": "1",
        "work_notes": "Se pasa la Release a New"
    }
    updated_record = release.update(query={'number': rls}, payload=update)
    print(updated_record)
    rls_id, rls_state = get_rls_status(rls=rls)


def update_cancel_rls_canceled(rls=number):
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    update = {
        "state": "Cancelled",
        "work_notes": "Se pasa la Release a New"
    }
    updated_record = release.update(query={'number': rls}, payload=update)
    print(updated_record)
    rls_id, rls_state = get_rls_status(rls=rls)



def check_rls_exist(rls=number):
    # Define a resource, here we'll use the release table API
    release = c.resource(api_path='/table/rm_release')

    response = release.get(query={'number': rls}, stream=True)
    # Iterate over the result and print out `sys_id` of the matching records.
    print(response)
    for record in response.all():
        if record['number']:
            print(record['number'], rls_text[record['state']])
            sys_id_local = record['sys_id']
            state_check = record['state']
            return sys_id_local, state_check
        else:
            print('Empty')


def get_change_status(rls=number):
    # Define a resource, here we'll use the release table API
    release = c.resource(api_path='/table/rm_release')
    response = release.get(query={'number': rls}, stream=True)
    # Iterate over the result and print out `sys_id` of the matching records.
    for record in response.all():
        # print(record['number'], record['u_change']['value'])
        return record['u_change']['value']


def get_open_task(rls=number, group=ASSIGNMENT_GROUP):
    task_list = []
    task = c.resource(api_path='/table/rm_task')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "15" or rls_state == "9" or rls_state == '5':
        response = task.get(query={'top_task.number': rls, 'state': '1', 'assignment_group.name': group},
                            stream=True)
        for record in response.all():
            # print(record['number'])
            task_list.append(record['number'])
        return task_list
    else:
        print("RLS state %s not Match with open Task" % rls_state)
