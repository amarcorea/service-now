from datetime import datetime, timedelta
from config import USER, PASSWORD, INSTANCE, EMAILUSER
from config_task import APPLICATION, ASSIGNMENT_GROUP, DESCRIPTION, ORDER, RELEASE, SHORT_DESCRIPTION, STATE_TO_RESOLVE, TECHNOLOGY, TOP_TASK, TYPE, VERSION
import pysnow
from dict_text import tsk_text

c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)

number = ''


def create_task(rls=number, enviroment="Pre-Production"):
    # Define a resource, here we'll use the incident table API
    task = c.resource(api_path='/table/rm_task')
    # Define Time date for rls management
    proposed_date = datetime.now()
    start_date = proposed_date + timedelta(minutes=30)
    end_date = proposed_date + timedelta(days=15)
    # Convert to string to parse Json
    proposed_date = proposed_date.strftime("%Y-%m-%d %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    # Set the payload
    new_record = {
        "top_task": TOP_TASK,
        "u_release": RELEASE,
        "start_date": start_date,
        "end_date": end_date,
        "short_description": SHORT_DESCRIPTION,
        "description": DESCRIPTION,
        "u_state_to_resolve": STATE_TO_RESOLVE,
        "type": TYPE,
        "assignment_group": ASSIGNMENT_GROUP,
        "order": ORDER,
        "u_technology": TECHNOLOGY,
        "u_version": VERSION,
        "u_application": APPLICATION
    }
    # Create a new incident record
    result = task.create(payload=new_record)
    for record in result.all():
        print(record['number'], record['state'])
        task_new = record['state']
        return task_new,


def create_delegate_task(
                         =number):
    # Define a resource, here we'll use the incident table API
    task = c.resource(api_path='/table/u_delegated_test')
    # Set the payload
    new_record = {
        "u_short_description": "Prueba delegada creada con API",
        "u_description": "Descripcion larga de la prueba delegada creada con API",
        "u_cycle": "1",
        "u_test_result": "OK",
        "u_parent": rls,
    }
    # Create a new incident record
    result = task.create(payload=new_record)
    for record in result.all():
        # print(record)
        print(record['u_number'])
        # task_new = record['state']
        return record['u_number']


def get_task_status(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    response = task.get(query={'number': tsk}, stream=True)
    for record in response.all():
        # print(record)
        state_check = record['state']
        print(tsk_text[record['state']])
        return state_check


def get_stask_status(tsk=number):
    task = c.resource(api_path='/table/sc_task')
    response = task.get(query={'number': tsk}, stream=True)
    for record in response.all():
        # print(record)
        state_check = record['state']
        print(tsk_text[record['state']])
        return state_check


def close_stask(tsk=number):
    task = c.resource(api_path='/table/sc_task')
    update = {
        "work_notes": "Reiniciado",
        "state": "Closed Complete",
        "assigned_to": EMAILUSER,

    }
    task_state = get_stask_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)


def close_task(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    update = {
        "work_notes": "Desplegado",
        "state": "Closed Complete",
        "u_close_code": "Successful automatic",
        "close_notes": "Desplegado en PRE-STG",
        "assigned_to": EMAILUSER,

    }
    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)


def close_test_task(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    update = {
        "state": "Closed Skipped",
        "u_close_code": "Successful automatic",
        "close_notes": "N/A",
        "assigned_to": USER,
        'u_performance_test_type': 'Unitary',
        'u_performance_result': 'OK',
    }
    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)


def attachment_task(tsk=number, file='requirements.txt'):
    task = c.resource(api_path='/table/rm_task')

    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5") and (task_state != "-7"):
        upload_record = task.get(query={'number': tsk})
        upload_record.upload(file_path=file)
        print(upload_record)
    else:
        print("Task %s Already Closed" % tsk)


def attachment_delegate_task(tsk=number, file='requirements.txt'):
    task = c.resource(api_path='/table/u_delegated_test')
    upload_record = task.get(query={'u_number': tsk})
    upload_record.upload(file_path=file)
    print(upload_record)


def cancel_task(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    update = {
        "work_notes": "Desplegado",
        "state": "Closed Skipped",
        "u_close_code": "Cancelled",
        "close_notes": "Problem in task",
        "assigned_to": EMAILUSER
    }
    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5") and (task_state != "7"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)
