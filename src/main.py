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

    ln = Learn(lnsettings)
    tm = TaskManager(tmsettings)
    print("Initialization complete.")
    
    ln.set_local()
    ln.login()
    print("Logged in.")

    tm.project_setup(ln.set_semester())
    print("Project setup complete.")

    tm.section_setup()
    print("Section setup complete.")

    print("Getting lessons and assignments...")
    lessons = ln.get_lessons()
    print("Lessons retrieved.")
    assignments = ln.get_ddl(lessons=lessons, download_files=False)
    print("Assignments retrieved.")

    print("Lessons:")
    for lesson in lessons:
        print(lesson)
    tm.init_courses(lessons)
    print("Courses initialized.")

    print("Assignments:")
    for assignment in assignments:
        print(assignment)
    tm.update_assignments(assignments)
    print("Assignments updated.")

    return path

def test():
    learn = Learn()
    learn.login()
    print(learn.set_semester())

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        # packaged environment
        temp_config_path = os.path.join(sys._MEIPASS, "config.json")
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