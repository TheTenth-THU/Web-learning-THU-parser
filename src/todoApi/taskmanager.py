""" File: todoApi/taskmanager.py

This module is responsible for managing the assignments in Todoist. The format of arguments is consistent with what `thulearn2018` uses.

We have the 3-level structure of the to-do list, i.e. `project` -> `section` -> `task` with `label`. Here, we use the following mapping:
.
└── 2024-2025-2 (`semester`)                # project
    ├── Assignments                         # section
    │   ├── task 1 with label `course`      # task
    │   └── task 2 with label `course`
    ├── Exams
    │   ├── task 1 with label `course`
    │   └── task 2 with label `course`
    └── Projects
        ├── task 1
        └── task 2
"""

from .todoist_interfaces import TodoistInterface

import sys
from tqdm import tqdm
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self, settings, reset=False):
        self.settings = settings
        self.todoist = TodoistInterface(self.settings, reset=reset)
        self.working_project = None
        self.working_section = None
        self.working_task = None

    def project_setup(self, semester: str):
        """ Set the working project to the specified semester.

        Args:
            semester (str): Semester id, e.g. `2024-2025-2`.
        """
        projects = self.todoist.get_projects()
        for project in projects:
            if project.name == semester:
                self.working_project = project
                return
        if self.working_project is None:
            self.working_project = self.todoist.add_project(semester)

    def section_setup(self, project_id: str = None):
        """ Initialize the sections for the working project or a specified project.
        
        Create 'Assignments', 'Exams' and 'Projects' sections in the working project or the specified project, and **set the working section to 'Assignments'**.

        Args:
            project_id (str): Project id to initialize sections. If not specified, the working project will be used.
        """
        if project_id is None:
            project_id = self.working_project.id
        if self.todoist.get_section(project_id, 'Exams') is None:
            self.todoist.add_section(project_id, 'Exams')
        if self.todoist.get_section(project_id, 'Projects') is None:
            self.todoist.add_section(project_id, 'Projects')
        self.working_section = self.todoist.get_section(project_id, 'Assignments')
        if self.working_section is None:
            self.working_section = self.todoist.add_section(project_id, 'Assignments')

    def init_courses(self, courses: list):
        """ Create labels for courses.

        Args:
            courses (list): List of course names.
        """
        if sys.stdout is not None and sys.stdout.isatty():
            # is in terminal
            prog_bar = tqdm(courses, desc='Creating labels')
        else:
            prog_bar = courses
        colors = self.settings.color_choices
        labels = [l.name for l in self.todoist.get_personal_labels()]
        count = 0
        for course in prog_bar:
            if sys.stdout is not None and sys.stdout.isatty():
                prog_bar.set_description(f'Creating label for course "{course[1]}"')
            if course[4] not in labels:
                self.todoist.add_label(course[1], color=colors[count])
                count = (count + 1) % len(colors)

    def update_assignments(self, assignments: list[list]):
        """ Add an assignment to the working section.

        This method will **create new tasks** for the assignments that are not in the working section, **update the due date and priority** for the assignments that are already in the working section, and **complete the tasks** for the assignments that are submitted. Submitted assignments which are not active in the working section will be ignored.

        Meanwhile, this method maintains `changed.txt` to record whether the due date of the assignment has been changed manually. If the due date on Todoist is different from the due date in `changed.txt`, the task will be considered as "changed" and will be never updated.

        Args:
            assignments (list[list]): List of assignments. Each assignment is a list of 5 elements, i.e. [_course_, _name_, _due_string_, _rest_time_, _submission_].
        """
        try:
            with open(self.settings.changed_file_path, 'r') as f:
                changed = f.readlines()
                # line format: `task_id || task_name || task_due || task_changed_flag\r\n`
                changed = {line.split(' || ')[1]: {'id': line.split(' || ')[0], 
                                                'due': datetime.strptime(line.split(' || ')[2], '%Y-%m-%dT%H:%M:%S'),
                                                'changed': (line.split(' || ')[3].replace('\r', '').replace('\n', '') == 'True')}
                        for line in changed}
        except:
            changed = {}
            print('Warning: No `changed.txt` found at {}. A new file will be created.'.format(self.settings.changed_file_path))

        exist_tasks = self.todoist.get_tasks(project_id=self.working_project.id, section_id=self.working_section.id)
        exist_tasks_due = {task.content: task.due.datetime for task in exist_tasks}
        exist_tasks_id = {task.content: task.id for task in exist_tasks}
        exist_tasks = [task.content for task in exist_tasks]

        labels = self.todoist.get_personal_labels()
        labels = {l.name: l for l in labels}

        if sys.stdout is not None and sys.stdout.isatty():
            # is in terminal
            prog_bar = tqdm(assignments, desc='Parsing assignments')
        else:
            prog_bar = assignments

        for assignment in prog_bar:
            # parse assignment info from Web Learning
            course, name, due_string, rest_time, submission = assignment
            if sys.stdout is not None and sys.stdout.isatty():
                prog_bar.set_description(f'Parsing assignment "{name}"')
            content = course + ' **' + name + '**'
            due_datetime = datetime.strptime(due_string, '%Y-%m-%d %H:%M')
            
            if due_datetime < datetime.now() + timedelta(days=3):
                priority = 3
            else:
                priority = 2

            if content in exist_tasks:
                # task has been added to Todoist
                if submission != '未交':
                    self.todoist.complete_task(self.todoist.get_task(self.working_project.id, content).id)
                else:
                    if changed.get(name) is not None:
                        if changed[name]['changed']:
                            due_string = changed[name]['due'].strftime('%Y-%m-%d %H:%M')
                        elif exist_tasks_due[content] != changed[name]['due']:
                            due_string = changed[name]['due'].strftime('%Y-%m-%d %H:%M')
                            changed[name]['changed'] = True
                        else:
                            changed[name]['due'] = due_datetime
                    else:
                        changed[name] = {'id': exist_tasks_id[content], 'due': due_datetime, 'changed': False}
                            
                    task = self.todoist.get_task(self.working_project.id, content)
                    if task.due.datetime != due_datetime.strftime('%Y-%m-%dT%H:%M:%S') or task.priority != priority:
                        self.todoist.update_task(task.id, due_string=due_string, priority=priority)
            else:
                if submission != '未交':
                    pass
                else:
                    new_task = self.todoist.add_task(
                        content,
                        self.working_project.id,
                        section_id=self.working_section.id,
                        due_string=due_string,
                        priority=priority,
                        labels=[labels[course].name]
                    )
                    changed[name] = {'id': new_task.id, 'due': new_task.due.datetime, 'changed': False}

        with open(self.settings.changed_file_path, 'w') as f:
            if sys.stdout is not None and sys.stdout.isatty():
                # is in terminal
                prog_bar = tqdm(changed.items(), desc='Saving assignments')
            else:
                prog_bar = changed.items()
            for name, info in prog_bar:
                # if info["due"] is str type
                if isinstance(info["due"], str):
                    print(f'{info["id"]} || {name} || {info["due"]} || {info["changed"]}', file=f)
                else:
                    print(f'{info["id"]} || {name} || {info["due"].strftime("%Y-%m-%dT%H:%M:%S")} || {info["changed"]}', file=f)
