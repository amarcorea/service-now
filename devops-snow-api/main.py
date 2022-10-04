import pysnow
import time
from rls import create_rls, get_rls_status, update_rls_cert, approve_rls_pre, update_rls_pre, update_rls_eval, \
    update_rls_test, approve_rls_eval, update_rls_scheduled, update_rls_implement, update_rls_closed, \
    update_cancel_rls_new, update_cancel_rls_canceled, get_open_task, get_change_status, check_rls_exist
from tasks import create_task, get_task_status, create_delegate_task, close_task, close_test_task, \
    attachment_task, cancel_task, attachment_delegate_task, get_stask_status, close_stask
from config import USER, PASSWORD, INSTANCE, RLS, TESTGROUP, STASK
from dict_text import rls_text, tsk_text

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ""


def create_release():
    sys_id, state, rls_number = create_rls()
    rls_id, rls_state = get_rls_status(rls=rls_number)
    # task = create_task(rls=rls_number)
    # task_pro = create_task(rls=rls_number,enviroment="Implement")
    return rls_number


def update_cert_pre_step2(RLS=RLS):
    update_rls_cert(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)
    update_rls_pre(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)


def approve_close_pre_step3(RLS=RLS):
    rls_id, rls_state = get_rls_status(rls=RLS)
    opent_task = get_open_task(rls=RLS)
    print(opent_task)
    try:
        for task in opent_task:
            close_task(tsk=task)
    except TypeError:
        print("Error There is no open Tasks")


def cancel_task_step10(RLS=RLS):
    rls_id, rls_state = get_rls_status(rls=RLS)
    opent_task = get_open_task(rls=RLS)
    print(opent_task)
    try:
        for task in opent_task:
            cancel_task(tsk=task)
            get_task_status(tsk=task)
    except TypeError:
        print("ERORR There is no open Tasks")


def update_close_task_test_step4(RLS=RLS):
    opent_task = get_open_task(rls=RLS, group=TESTGROUP)
    print(opent_task)
    for task in opent_task:
        close_test_task(tsk=task)
    rls_id, rls_state = get_rls_status(rls=RLS)


def close_stask_step1(tsk=STASK):
    get_stask_status(tsk=tsk)
    close_stask(tsk=tsk)
    get_stask_status(tsk=tsk)


if __name__ == '__main__':
    # RLS = create_release()
    # update_cert_pre_step2(RLS=RLS)
    # get_rls_status(rls=RLS)
    # approve_rls_pre(rls=RLS)
    # approve_close_pre_step3(RLS=RLS)
    # create_task(rls=RLS)
    # opent_task = get_open_task(rls=RLS)
    # print(opent_task)
    # close_task(tsk='RTSK0972819')
    # for task in opent_task:
    #     # time.sleep(10)
    #     close_task(tsk=task)
    #     time.sleep(5)
    # update_rls_test(rls=RLS)
    # update_close_task_test_step4(RLS=RLS)
    # create_rls()
    # get_rls_status(rls=RLS)
    # # create_task(rls=RLS)
    # update_rls_cert(rls=RLS)
    # update_rls_pre(rls=RLS)
    close_stask_step1(tsk=STASK)
    # update_rls_eval(rls=RLS)
    # approve_rls_eval(rls=RLS)
    # approve_rls_eval(rls=RLS)
    # update_rls_scheduled(rls=RLS)
    # get_rls_status(rls=RLS)
    # opent_task = get_open_task(rls=RLS)
    # print(opent_task)
    # for task in opent_task:
    #     close_task(tsk=task)
    # update_rls_implement(rls=RLS)
    # update_rls_closed(rls=RLS)
    # get_rls_status(rls=RLS)
