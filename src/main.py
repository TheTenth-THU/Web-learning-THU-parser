from thulearn2018.browser import Learn
from todoApi.taskmanager import TaskManager

from thulearn2018.settings import Settings as lnSettings
from todoApi.settings import Settings as tmSettings

import os
import sys
import json
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

def main(path=None):
    if not path:
        print("You can specify where to save the configuration files. If you don't, it will be saved in ")
        print("    C:\\Users\\<username>\\Documents\\WebLearningTHU\\.config for Windows, ")
        print("    ~/.config/WebLearningTHU/                            for Linux, ")
        print("    ~/Library/Application Support/WebLearningTHU/.config for macOS.")
        print("Input the path to save the configuration files (w/o '.config' folder, 'Enter' to use default):")
        path = prompt("Path: ", completer=PathCompleter())
    path = os.path.abspath(path) if path else None
    lnsettings = lnSettings(path)
    tmsettings = tmSettings(path)

    reset = (sys.stdin is not None) and (sys.stdin.isatty()) and (sys.stdout is not None) 
    if reset:
        print("Reset mode accessible. ")
        reset = input("Use reset mode to input the path and port manually? ([Y]/n) ") in ['', 'Y', 'y']

    ln = Learn(lnsettings, reset=reset)
    tm = TaskManager(tmsettings, reset=reset)
    print("Initialization complete.")
    print("=================================================")

    ln.set_local()
    ln.login()
    print("Logged in.")
    print("=================================================")

    tm.project_setup(ln.set_semester())
    print("Project setup complete.")

    tm.section_setup()
    print("Section setup complete.")

    print("Getting lessons and assignments...")
    try:
        lessons = ln.get_lessons()
        print("Lessons retrieved.")
        assignments = ln.get_ddl(lessons=lessons, download_files=True)
        print("Assignments retrieved.")
    except Exception as e:
        print(f"Error: Failed to get lessons and assignments, {e}")
        if reset:
            input("Press Enter to exit...")
        sys.exit(1)
    print("=================================================")

    try:
        print(f"Get {len(lessons)} Lesson(s):")
        for lesson in lessons:
            print("\t".join(lesson))
        tm.init_courses(lessons)
        print("Courses initialized.")
        print("=================================================")

        print(f"Get {len(assignments)} Assignment(s):")
        for assignment in assignments:
            assign = assignment[:-1] + ["..."]
            print("\t".join(assign))
        tm.update_assignments(assignments)
        print("Assignments updated.")
        print("=================================================")
    except Exception as e:
        print(f"Error: Failed to initialize courses or update assignments, {e}")
        if reset:
            input("Press Enter to exit...")
        sys.exit(1)

    # write the configurations into a temporary file
    if (os.name == 'nt'):
        temp_dir = os.path.join(os.environ.get("APPDATA"), "temp_WebLearningTHU", ".temp")
    elif (os.name == 'posix'):
        temp_dir = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "temp_WebLearningTHU", ".temp")
    else:
        temp_dir = os.path.join(Path.home(), "temp_WebLearningTHU", ".temp")

    file_path = ln.fm.get_path(reset=False)
    file_port = ln.settings.port
    while not file_path:
        print("Warning: Failed to get the path from with_console.exe.")
        if reset:
            # console can be used, use Prompt Toolkit to input the path
            print("You can manually input the path where assignments are saved: ")
            file_path = prompt("Path: ", completer=PathCompleter())
        else:
            # no console can be used to input the path, just exit
            sys.exit(1)
    while not file_port:
        print("Warning: Failed to get the port from with_console.exe.")
        if reset:
            # console can be used to input the port
            file_port = input("You can manually input the port you just set in the console: ")
        else:
            # no console can be used to input the port, just exit
            sys.exit(1)
            
    try:
        if not os.path.exists(os.path.dirname(temp_dir)):
            os.makedirs(os.path.dirname(temp_dir))
        with open(temp_dir, 'w') as f:
            print(file_path, file=f)
            print(file_port, file=f)
    except Exception as e:
        print(f"Error: Failed to write the path '{file_path}' and port '{file_port}' to {temp_dir}, {e}")
    else:
        print(f"Path and port written to {temp_dir}.")
        
    print("All done. ")
    if reset:
        input("Press Enter to exit...")
    return path

def test():
    learn = Learn()
    learn.login()
    print(learn.set_semester())

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        # packaged environment
        user_docs = os.path.join(os.path.expanduser("~"), "Documents")
        config_dir = os.path.join(user_docs, "WebLearningTHU")
        temp_config_path = os.path.join(config_dir, "config.json")
    else:
        # development environment
        temp_config_path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], "config.json")
    if not os.path.exists(os.path.split(temp_config_path)[0]):
        os.makedirs(os.path.split(temp_config_path)[0])
    if os.path.exists(temp_config_path):
        with open(temp_config_path, 'r') as f:
            config = json.load(f)
        if 'config_path' in config:
            path = config['config_path']
            path = main(path)
        else:
            path = main()
    else:
        path = main()
    with open(temp_config_path, 'w') as f:
        json.dump({'config_path': path}, f)