from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import (
    Collaborator,
    Comment,
    CompletedItems,
    Label,
    Project,
    QuickAddResult,
    Section,
    Task,
)
from datetime import datetime
from typing import List, Optional
import os

def authorize(settings, reset=False) -> str:
    """Authorize the user with the Todoist API token.

    If the user has authorized before, the stored API token will be used, and the user can change it if needed.

    Args:
        reset (bool):   Whether to reset the stored API token if it exists. Default is `False`.

    Returns:
        Auth_key (str): The Todoist API token.
    """
    auth_key = settings.get_auth()
    print("You can obtain your personal API token from https://todoist.com/prefs/integrations for Todoist.")
    if auth_key and reset:
        print("Input your personal API token: ('Enter' to skip change)")
        new_auth_key = input()
        if new_auth_key:
            auth_key = new_auth_key
            settings.set_auth(auth_key)
    elif not auth_key:
        print("Input your personal API token:")
        auth_key = input()
        while not auth_key:
            print("Input your personal API token:")
            auth_key = input()
        settings.set_auth(auth_key)
    return auth_key

class TodoistInterface:
    """The interface to interact with Todoist.
    """
    def __init__(self, settings, reset=False):
        self.settings = settings
        self.todoist = TodoistAPI(authorize(self.settings, reset=reset))

    ##################### PROJECT MANAGEMENT #####################

    def get_projects(self) -> List[Optional[Project]]:
        """ Get all projects.

        Returns:
            res (list[Project]):    A list of projects.
        """
        try:
            return self.todoist.get_projects()
        except Exception as e:
            print("Get projects failed:", e)
            return []
        
    def get_project(self, name: str) -> Optional[Project]:
        """ Get the project with the specified name.

        Args:
            name (str):         The name of the project.

        Returns:
            res (Project):      The project.
        """
        projects = self.get_projects()
        for project in projects:
            if project.name == name:
                return project
        return None

    def add_project(self, name: str) -> Optional[Project]:
        """ Add a project with the specified name.

        Args:
            name (str):         The name of the project.

        Returns:
            res (Project):      The added project.
        """
        try:
            return self.todoist.add_project(name)
        except Exception as e:
            print("Add project failed:", e)
            return None
        
    def favorite_project(self, project_id: str, to_favorite: bool = True) -> bool:
        """ Favorite the project with the specified id.

        Args:
            project_id (str):       The id of the project.
            to_favorite (bool):     Whether to favorite the project.

        Returns:
            res (Project):      The favorited project.
        """
        try:
            is_success = self.todoist.update_project(project_id=project_id, is_favorite=to_favorite)
            if not is_success:
                print("Favorite project failed by unknown reason.")
            return is_success
        except Exception as e:
            print("Favorite project failed:", e)
            return False

    ##################### SECTION MANAGEMENT #####################

    def get_sections(self, project_id: str) -> List[Optional[Section]]:
        """ Get all sections of the project with the specified id.

        Args:
            project_id (str):       The id of the project.

        Returns:
            res (list[Section]):    A list of sections.
        """
        try:
            return self.todoist.get_sections(project_id=project_id)
        except Exception as e:
            print("Get sections failed:", e)
            return []    
    
    def get_section(self, project_id: str, name: str) -> Optional[Section]:
        """ Get the section with the specified name of the project with the specified id.

        Args:
            project_id (str):       The id of the project.
            name (str):             The name of the section.

        Returns:
            res (Section):          The section.
        """
        sections = self.get_sections(project_id)
        for section in sections:
            if section.name == name:
                return section
        return None
    
    def add_section(self, project_id: str, name: str) -> Optional[Section]:
        """ Add a section with the specified name to the project with the specified id.

        Args:
            project_id (str):       The id of the project.
            name (str):             The name of the section.

        Returns:
            res (Section):          The added section.
        """
        try:
            return self.todoist.add_section(project_id=project_id, name=name)
        except Exception as e:
            print("Add section failed:", e)
            return None
    
    ##################### TASK MANAGEMENT #####################

    def get_tasks(self, project_id: str, section_id: str = None, label: str = None) -> List[Optional[Task]]:
        """ Get all tasks of the project with the specified id.

        Args:
            project_id (str):       The id of the project.
            section_id (str):       The id of the section.
            label (str):            The label of the task.

        Returns:
            res (list[Task]):       A list of tasks.
        """
        kwargs = {"project_id": project_id}
        if section_id:
            kwargs["section_id"] = section_id
        if label:
            kwargs["label"] = label
        try:
            return self.todoist.get_tasks(**kwargs)
        except Exception as e:
            print("Get tasks failed:", e)
            return []
        
    def get_task(self, project_id: str, title: str, section_id: str = None, label: str = None) -> Optional[Task]:
        """ Get the task with the specified content of the project with the specified id.

        Args:
            project_id (str):       The id of the project.
            content (str):          The content of the task.
            section_id (str):       The id of the section.
            label (str):            The label of the task.

        Returns:
            res (Task):             The task.
        """
        tasks = self.get_tasks(project_id, section_id, label)
        for task in tasks:
            if task.content == title:
                return task
        return None
    
    def add_task(self, 
                 title: str, 
                 project_id: str, 
                 section_id: str = None, 
                 labels: list[str] = [], 
                 desc: str = '',
                 **kwargs) -> Optional[Task]:
        """ Add a task with the specified content to the project with the specified id.

        Args:
            project_id (str):       The id of the project. This is a required argument.
            title (str):            The content of the task. This is a required argument.
            section_id (str):       The id of the section.
            labels (list[str]):     The labels of the task.
            desc (str):             The description of the task.
            priority (int):         The priority of the task, from 1 (normal) to 4 (urgent).
            parent_id (str):        The id of the parent task.
            order (int):            The order of the task among the tasks under the same parent task.
            due_string (str):       The due date of the task and can be recognized by Todoist.
            due_lang (str):         The language of the `due_string`. Default is `en`.
            due_datetime (str):     The due date of the task in _RFC3339_ format (`YYYY-MM-DDTHH:MM:SS`).

        Returns:
            res (Task):             The added task.
        """
        kwargs["project_id"] = project_id
        if section_id:
            kwargs["section_id"] = section_id
        if labels:
            kwargs["labels"] = labels
        if desc:
            kwargs["desc"] = desc
        if "due_datetime" in kwargs:
            kwargs["due_datetime"] = datetime.strptime(kwargs["due_datetime"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
            if "due_string" in kwargs:
                del kwargs["due_string"]
            if "due_lang" in kwargs:
                del kwargs["due_lang"]
        if "priority" in kwargs:
            if kwargs["priority"] < 1:
                kwargs["priority"] = 1
            elif kwargs["priority"] > 4:
                kwargs["priority"] = 4
            else:
                kwargs["priority"] = int(kwargs["priority"])
        try:
            return self.todoist.add_task(content=title, **kwargs)
        except Exception as e:
            print("Add task failed:", e)
            return None
        
    def complete_task(self, task_id: str) -> bool:
        """ Complete the task with the specified id.

        Args:
            task_id (str):          The id of the task.

        Returns:
            res (bool):             Whether the task is completed.
        """
        try:
            is_success = self.todoist.close_task(task_id)
            if not is_success:
                print("Complete task failed by unknown reason.")
            return is_success
        except Exception as e:
            print("Complete task failed:", e)
            return False
        
    ##################### LABEL MANAGEMENT #####################

    def get_personal_labels(self) -> List[Optional[Label]]:
        """ Get all personal labels.

        Returns:
            res (list[Label]):      A list of labels.
        """
        try:
            return self.todoist.get_labels()
        except Exception as e:
            print("Get labels failed:", e)
            return []
        
    def get_label(self, name: str) -> Optional[Label]:
        """ Get the label with the specified name.

        Args:
            name (str):         The name of the label.

        Returns:
            res (Label):        The label.
        """
        labels = self.get_personal_labels()
        for label in labels:
            if label.name == name:
                return label
        return None
    
    def add_label(self, name: str, color: str = 'grey') -> Optional[Label]:
        """ Add a label with the specified name.

        Args:
            name (str):         The name of the label.
            color (str):        The color of the label. Choices are _berry_red_, _red_, _orange_, _yellow_, _olive_green_, _lime_green_, _green_, _mint_green_, _teal_, _sky_blue_, _light_blue_, _blue_, _grape_, _violet_, _lavender_, _magenta_, _salmon_, _charcoal_, _grey_, _taupe_. Default is _grey_.

        Returns:
            res (Label):        The added label.
        """
        if color not in self.settings.color_choices:
            color = 'grey'
        try:
            return self.todoist.add_label(name=name, color=color)
        except Exception as e:
            print("Add label failed:", e)
            return None