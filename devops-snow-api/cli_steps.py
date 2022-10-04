from main import create_release, update_cert_pre_step2, approve_close_pre_step3, cancel_task_step10, update_close_task_test_step4, close_stask_step1
from rls import approve_rls_pre, update_rls_test, update_rls_scheduled, update_rls_implement, update_cancel_rls_new, get_rls_status
from tasks import close_test_task
from config import *
import getopt, sys

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hcuatoiprgnfs:"

# Long options
long_options = [
    "help", "get-release-status", "create-release", "update-to-pre",
    "approve-pre", "close-pre-task", "update-to-test",
    "update-to-implement", "close-pro-task", "update-to-review",
    "back-to-new", "fail-task", "close-stask"
]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--help"):
            print("Displaying Help")

        elif currentArgument in ("-g", "--get-release-status"):
            get_rls_status(rls=RLS)

        elif currentArgument in ("-c", "--create-release"):
            create_release()

        elif currentArgument in ("-u", "--update-to-pre"):
            print("Update RLS to PRE")
            update_cert_pre_step2(RLS=RLS)

        elif currentArgument in ("-a", "--approve-pre"):
            print("Approve RLS to PRE")
            approve_rls_pre(rls=RLS)

        elif currentArgument in ("-t", "--close-pre-task"):
            print("Close all Open TASK RLS in PRE")
            approve_close_pre_step3(RLS=RLS)

        elif currentArgument in ("-o", "--update-to-test"):
            update_rls_test(rls=RLS)
            update_close_task_test_step4(RLS=RLS)

        elif currentArgument in ("-i", "--update-to-implement"):
            print("Update RLS to Implementation")
            update_rls_scheduled(rls=RLS)

        elif currentArgument in ("-p", "--close-pro-task"):
            print("Close all Open RLS in PRE")
            approve_close_pre_step3(RLS=RLS)

        elif currentArgument in ("-r", "--update-to-review"):
            print("Update RLS to Implementation")
            update_rls_implement(rls=RLS)

        elif currentArgument in ("-n", "--back-to-new"):
            print("Wrong Parameters Back to New. Please Review!!")
            update_cancel_rls_new(rls=RLS)

        elif currentArgument in ("-n", "--fail-task"):
            print("Wrong Parameters Back to New. Please Review!!")
            cancel_task_step10(RLS=RLS)
            update_cancel_rls_new(rls=RLS)

        elif currentArgument in ("-s", "--close-stask"):
            print("Close all Open STASK")
            close_stask_step1(tsk=STASK)

except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
