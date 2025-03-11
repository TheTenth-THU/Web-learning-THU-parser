import os
import sys
import ctypes
import subprocess
import http.server
import ssl
import threading
import time

try:
    from ctypes import windll
    CREATE_NEW_CONSOLE = 0x00000010
except ImportError:
    CREATE_NEW_CONSOLE = 0



##################### Administrator Privileges #####################

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


##################### SUBPROCESS OUTPUT REDIRECTION #####################

def read_subprocess_output(proc, outlines):
    """ Read subprocess output line by line and print to the current terminal. """
    for line in proc.stdout:
        # print to the current terminal
        # print(line, end='')
        # store the last two lines
        if line.strip():
            outlines.append(line)
            if len(outlines) > 2:
                outlines.pop(0)
    # cycle ends when the child output stream is closed
    proc.wait()


##################### HTTPS Server #####################

class HTTPSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=returned_path, **kwargs)

    def do_GET(self):
        if self.path == "/favicon.ico":
            try:
                if hasattr(sys, '_MEIPASS'):
                    # after packaging
                    icon_path = os.path.join(sys._MEIPASS, "logo.ico")
                else:
                    # before packaging
                    icon_path = os.path.abspath("res\\logo.ico")
                with open(icon_path, 'rb') as f:
                    icon = f.read()
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.send_header("Content-Length", str(len(icon)))
                self.end_headers()
                self.wfile.write(icon)
            except Exception as e:
                self.send_error(404, f'File not found: {self.path}')
        else:
            return super().do_GET()

server_holder = []

def run_https_server(returned_port, cert_file, key_file) -> http.server.HTTPServer:
    """ Run an HTTPS server to serve local files. """
    httpd = http.server.HTTPServer(('localhost', int(returned_port)), HTTPSHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=cert_file, keyfile=key_file)
    print(f"Serving HTTPS on https://localhost:{returned_port}")
    server_holder.append(httpd)
    httpd.serve_forever()
    return httpd


##################### Main #####################

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
    "/MO", "1",
    "/TN", task_name,
    "/TR", f'"{without_console_path}"',
    "/F"
]

# create scheduled task to run without_console.exe every 3 hours
print("Creating scheduled task...")
result = subprocess.run(" ".join(schtask_cmd), shell=True)
if result.returncode != 0:
    print("Error: Failed to create scheduled task.")
else:
    print("Scheduled task created successfully.")

# run with_console.exe
with_console_path = os.path.join(base_dir, "with_console.exe")
print("Launching with_console.exe in new console...")
try:
    proc = subprocess.Popen(
        [with_console_path], 
        cwd=base_dir,
        creationflags=CREATE_NEW_CONSOLE    # new console window for Windows
    )
    proc.wait()
    outlines = []
    # read_thread = threading.Thread(
    #     target=read_subprocess_output, 
    #     args=(proc, outlines),
    #     daemon=True
    # )
    # read_thread.start()
    # print("Launched with_console.exe.")
    # read_thread.join()
    if (os.name == 'nt'):
        temp_dir = os.path.join(os.environ.get("APPDATA"), "temp_WebLearningTHU", ".temp")
    elif (os.name == 'posix'):
        temp_dir = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "temp_WebLearningTHU", ".temp")
    else:
        temp_dir = os.path.join(Path.home(), "temp_WebLearningTHU", ".temp")
    with open(temp_dir, 'r') as f:
        outlines = f.readlines()
        outlines = [x.strip() for x in outlines]
    os.remove(temp_dir)
    print("Launched with_console.exe.")
except Exception as e:
    print(f"Error: Failed to run with_console.exe, {e}")
    input("Press Enter to exit...")
    sys.exit(1)

print("Your Web Learning tasks have been imported to Todoist, and it will be updated every 3 hours.")

if len(outlines) == 2:
    returned_path = outlines[0].strip()
    returned_port = outlines[1].strip()
    print(f"Captured path {returned_path}, and port {returned_port}.")
else:
    print("Warning: Failed to get the path and port from with_console.exe.")
    input("Press Enter to exit...")
    sys.exit(1)

# set OPENSSL_CONF environment variable
os.environ["OPENSSL_CONF"] = os.path.abspath("D:\\Program Files (x86)\\Git\\usr\\ssl\\openssl.cnf")

# create certificate and key files
cert_file = os.path.join(base_dir, "cert.pem")
key_file = os.path.join(base_dir, "key.pem")
if not os.path.exists(cert_file) or not os.path.exists(key_file):
    print("Creating certificate and key files...")
    result = subprocess.run(
        f"openssl req -new -x509 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj /CN=localhost",
        shell=True
    )
    if result.returncode != 0:
        print("Error: Failed to create certificate and key files.")
        input("Press Enter to exit...")
        sys.exit(1)

# run HTTPS server
print("Starting HTTPS server for local file fetching...")
thread = threading.Thread(target=run_https_server, args=(returned_port, cert_file, key_file))
thread.daemon = True
thread.start()

time.sleep(1)
input("Press Enter to exit...")

# close the HTTPS server
if len(server_holder):
    for server in server_holder:
        server.shutdown()
thread.join()
print("HTTPS server closed.")
print("Exiting the program.")
sys.exit(0)