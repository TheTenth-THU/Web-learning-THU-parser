import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    # re-run the program with admin rights using the runas verb
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)

if not is_admin():
    print("Requesting for administrator privileges...")
    run_as_admin()

# delete scheduled task with name "TsinghuaWebLearning2Todoist"
task_name = "TsinghuaWebLearning2Todoist"
delete_cmd = ["schtasks", "/Delete", "/TN", task_name, "/F"]

print("Deleting scheduled task...")
result = subprocess.run(" ".join(delete_cmd), shell=True)
if result.returncode != 0:
    print("Error: Failed to delete scheduled task.")
else:
    print("Scheduled task deleted successfully.")

print("Your Web Learning tasks on Todoist will not be updated anymore.")
input("Press any key to exit...")