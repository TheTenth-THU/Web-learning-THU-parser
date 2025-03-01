import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    # re-run the program with admin rights using the runas verb
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)

if not is_admin():
    print("Requesting for administrator privileges...")
    run_as_admin()

if hasattr(sys, '_MEIPASS'):
    # after packaging: sys.executable points to the exe file
    base_dir = os.path.abspath(os.path.dirname(sys.executable))
else:
    # before packaging
    base_dir = os.path.abspath("./dist/")

task_name = "TsinghuaWebLearning2Todoist"
without_console_path = os.path.join(base_dir, "without_console.exe")
schtask_cmd = [
    "schtasks", "/Create",
    "/SC", "HOURLY",
    "/MO", "3",
    "/TN", task_name,
    "/TR", f'"{without_console_path}"',
    "/F"
]

print("Creating scheduled task...")
result = subprocess.run(" ".join(schtask_cmd), shell=True)
if result.returncode != 0:
    print("Error: Failed to create scheduled task.")
else:
    print("Scheduled task created successfully.")

with_console_path = os.path.join(base_dir, "with_console.exe")
print("Launching with_console.exe...")
try:
    proc = subprocess.Popen([with_console_path], cwd=base_dir)
    proc.wait()  # Wait until the process finishes
except Exception as e:
    print(f"Error: Failed to run with_console.exe, {e}")

print("Your Web Learning tasks have been imported to Todoist, and it will be updated every 3 hours.")
input("Press any key to exit...")