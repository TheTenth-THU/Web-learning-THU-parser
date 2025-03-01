<div align="center">
  <div>
      <img src="res/logo.png" width="128" height="128">
  </div>
  <h1>Todoist Adapter for Tsinghua University Web Learning</h1>
  <h2>针对华清大学网络学堂的 Todoist 适配工具</h2>
  <table>
    <tr>
      <td><a href="README.md">中文</a></td>
      <td style="font-weight: bold;">English</td>
      <td><a href="README_ru.md">Русский</a></td>
    </tr>
  </table>
</div>

## Introduction

This repository is a Todoist adapter designed for Tsinghua University's Web Learning platform. It parses the course and assignment lists from the platform and converts them into Todoist tasks.

<details>
<summary style="font-size: 1.2em; font-weight: bold;">
  Project Foundations
</summary>

### Todoist REST API

Todoist is a task management tool comparable to MS To-Do in its free version. It provides a REST API for developers to interact with the Todoist server via HTTP requests, as well as a Python SDK for easier development.

+ Homepage: [https://todoist.com/](https://todoist.com/)
+ REST API Documentation: [https://developer.todoist.com/rest/v2/](https://developer.todoist.com/rest/v2/)

### euxcet/thulearn2018

This repository modifies the unofficial tool for Tsinghua University's Web Learning platform originally available at euxcet/thulearn2018. The `browser` module in that project offers comprehensive parsing functionalities to fetch course and assignment lists.

+ GitHub Repository: [![GitHub stars](https://img.shields.io/github/stars/euxcet/thulearn2018?style=social)](https://github.com/euxcet/thulearn2018)

</details>

## Structure

### Project Structure

```plaintext
./
├── README.md
├── README_en.md
├── README_ru.md
├── src/
│   ├── main.py                   # Entry point
│   ├── thulearn2018/             # euxcet/thulearn2018 
│   │   │                             project modules
│   │   ├── __init__.py
│   │   ├── browser.py
│   │   ├── filemanager.py
│   │   ├── jsonhelper.py
│   │   ├── learn.py
│   │   ├── settings.py
│   │   ├── soup.py
│   │   └── utils.py
│   └── todoApi/                  # Todoist API wrapper
│       ├── settings.py
│       ├── taskmanager.py
│       └── todoist_interfaces.py
└── packager/
  ├── with_console.ps1
  └── without_console.ps1
```

### Release File Structure

```plaintext
Web-Learning-THU-Parser/
├── launchar.bat            # Recommended startup script; 
│                           #   configures settings and 
│                           #   adds a scheduled task
├── deleter.bat             # Deletes the scheduled task
├── with_console.exe        # Executable with a console window
└── without_console.exe     # Executable without a console window
```

#### with_console.exe and without_console.exe

Both executables are packaged versions of `main.py` and can be run directly. Their respective packaging scripts are located in `packager/with_console.ps1` and `packager/without_console.ps1`.
+ `with_console.exe` opens a console window so that you can configure settings and view logs.
+ `without_console.exe` does not open a console window, so logs cannot be viewed; if configuration is incomplete or incorrect, errors will occur.

If you encounter errors when running `without_console.exe`, try running `with_console.exe` to view error messages or complete the configuration.

#### launchar.bat

`launchar.bat` is a batch file that adds `without_console.exe` to the Windows Scheduled Tasks to run every 3 hours. After adding the task, it runs `with_console.exe` for configuration.

When you double-click `launchar.bat`, it prompts for administrator privileges to add `without_console.exe` to the scheduled tasks.

#### deleter.bat

`deleter.bat` is a batch file used to remove `without_console.exe` from the Windows Scheduled Tasks.

## Usage

### Direct Usage

#### 1. Register on Todoist

First, you need to register for a Todoist account. You can register on the [Todoist homepage](https://todoist.com/) or download the Todoist client.

> **Note**: For Android users, Todoist can be downloaded from the Google Play Store. If you are unable to access the store, try using [Aurora Store](https://auroraoss.com/) or download the APK from [APKMirror](https://www.apkmirror.com/).

#### 2. Download the Latest Release

Visit the [Release page](https://github.com/TheTenth-THU/Web-learning-THU-parser/releases) of this repository to download the latest zip file, then extract it to your desired location. **Do not move, delete, or modify any files within the extracted folder.**

#### 3. Run launchar.bat

Double-click `launchar.bat` in the extracted folder. A prompt will request administrator privileges to add `without_console.exe` to the scheduled tasks, ensuring it runs periodically.

Once privileges are granted, `with_console.exe` will open a console window where you can input your Todoist API Token, configuration file save path, Web Learning username, password, and other information as prompted.

### For Developers

This project modifies parts of the euxcet/thulearn2018 tool and adds extensive docstring annotations, which may be helpful for further development. Additionally, this project provides a wrapper for the Todoist REST API for easier integration.

#### Dependency Configuration

This project requires Python:
+ **3.7 and above** to support the new SSL renegotiation features.
+ **Up to 3.9**, to maintain compatibility with SSL renegotiation.

The development and testing environment for this project is **Python 3.9.13**. You can use tools like Anaconda or [pyenv](https://github.com/pyenv/pyenv) ([pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows) to create a virtual environment with the required version.

Install the project dependencies using:

```shell
pip install -r requirements.txt
```

#### Module Overview

<details>
<summary style="font-weight: bold;">
  thulearn2018/
</summary>

<details>
<summary style="font-style: italic;">
  thulearn2018.settings
</summary>

The `thulearn2018.settings` module provides the `Settings` class for managing configuration information.

| Category      | Method                    | Parameters                          | Return   | Description                     |
| ------------- | ------------------------- | ----------------------------------- | -------- | ------------------------------- |
| Initialization| `Settings.__init__`       | `path`: _str_ (path to config file) | _None_   | Initializes a `Settings` instance |
</details>

<details>
<summary style="font-style: italic;">
  thulearn2018.browser
</summary>

The `thulearn2018.browser` module integrates functionalities to parse course lists and assignment lists from the Web Learning platform, providing the `Learn` class.

| Category          | Method                       | Parameters                     | Return        | Description                         |
| ----------------- | ---------------------------- | ------------------------------ | ------------- | ------------------------------------ |
| Initialization    | `Learn.__init__`             | `settings`: _Settings_ instance| _None_        | Initializes the `Learn` class         |
|                   |                              | `reset`: _bool_ (whether to re-enter username and password) |      |                                      |
| User Management   | `Learn.set_user`             | _None_                         | _None_        | Sets the Web Learning username and password |
|                   | `Learn.get_user`             | _None_                         | _str_         | Retrieves current username and password |
| File Management   | `Learn.set_path`             | _None_                         | _None_        | Sets the path for saving files         |
|                   | `Learn.get_path`             | _None_                         | _str_         | Retrieves the current file path        |
|                   | `Learn.set_local`            | _None_                         | _None_        | Resets (clears) local file records      |
| Network Management| `Learn.login`                | `mode`: _str_ (login mode)      | _None_        | Logs into the platform using credentials |
| Course Management | `Learn.set_semester`         | `semester`: _str_ (semester ID) | _None_        | Sets the current semester               |
|                   | `Learn.get_lessons`          | `exclude`: _list_ (courses to exclude) | _list_   | Retrieves the course list for the current semester |
|                   |                            | `include`: _list_ (courses to include)  |             |                                      |
|                   | `Learn.init_lessons`         | `exclude`: _list_ (courses to exclude) | _list_   | Creates directories for courses       |
|                   |                            | `include`: _list_ (courses to include)  |             |                                      |
| Assignment Management | `Learn.get_files_id`     | `lesson_id`: _str_ (course ID)   | _list_        | Retrieves a list of file IDs for the course |
|                   | `Learn.file_id_exist`        | `fid`: _str_ (file ID)           | _bool_        | Checks if a file ID exists locally      |
|                   | `Learn.save_file_id`         | `fid`: _str_ (file ID)           | _None_        | Saves the file ID locally             |
|                   | `Learn.download_files`       | `lesson_id`: _str_ (course ID)   | _None_        | Downloads course files                |
|                   |                            | `lesson_name`: _str_ (course name) |            |                                      |
|                   |                            | `file_id`: _str_ (file ID)       |             |                                      |
|                   | `Learn.download_homework`    | `lesson_id`: _str_ (course ID)   | _list_        | Downloads assignments for the course |
|                   |                            | `lesson_name`: _str_ (course name) |            |                                      |
|                   |                            | `download_submission`: _bool_ (download submitted assignments) | |                                  |
|                   |                            | `download_files`: _bool_ (download files) |       |                                  |
|                   | `Learn.upload`               | `homework_id`: _str_ (assignment ID) | _None_   | Uploads assignment files              |
|                   |                            | `file_path`: _str_ (file path)   |             |                                      |
|                   |                            | `message`: _str_ (upload message)|            |                                      |
|                   | `Learn.get_ddl`              | `lessons`: _list_ (course list)  | _list_        | Retrieves assignment deadlines       |
|                   |                            | `download_submission`: _bool_ (download submitted assignments) | |                                  |
|                   |                            | `download_files`: _bool_ (download files) |       |                                  |
</details>

<details>
<summary style="font-style: italic;">
  thulearn2018.learn
</summary>

The `thulearn2018.learn` module provides a command line interface (CLI) for interacting with Tsinghua University's Web Learning platform. It uses the `click` library to implement commands such as downloading course files, resetting configuration, displaying configuration, clearing download records, submitting assignments, and showing assignment deadlines.

| Category         | Command           | Parameters                                  | Return    | Description                                               |
| ---------------- | ----------------- | ------------------------------------------- | --------- | --------------------------------------------------------- |
| Download         | `download`        | `exclude`: _str_ (courses to exclude)       | _None_    | Downloads all course files for the specified courses and semester |
|                  |                   | `include`: _str_ (courses to include)       |           |                                                           |
|                  |                   | `semester`: _str_ (semester ID)             |           |                                                           |
|                  |                   | `path`: _str_ (file save path)               |           |                                                           |
|                  |                   | `download_submission`: _bool_ (download submitted assignments) | |                                        |
| Reset            | `reset`           | _None_                                      | _None_    | Resets configuration such as username and file path     |
| Display Config   | `config`          | _None_                                      | _None_    | Displays current configuration, including username and file path |
| Clear Records    | `clear`           | `semester`: _str_ (semester ID)             | _None_    | Clears all download records for the specified semester    |
| Submit Assignment| `submit`          | `name`: _str_ (assignment file path)         | _None_    | Submits the specified assignment along with a message     |
|                  |                   | `m`: _str_ (submission message)              |           |                                                           |
| Show Deadlines   | `ddl`             | `exclude`: _str_ (courses to exclude)       | _None_    | Displays assignment deadlines for the specified courses and semester |
|                  |                   | `include`: _str_ (courses to include)       |           |                                                           |
|                  |                   | `semester`: _str_ (semester ID)             |           |                                                           |
|                  |                   | `path`: _str_ (assignment file save path)    |           |                                                           |
|                  |                   | `download_submission`: _bool_ (download submitted assignments) | |                                        |
</details>
</details>

<details>
<summary style="font-weight: bold;">
  todoApi/
</summary>

<details>
<summary style="font-style: italic;">
  todoApi.settings
</summary>

The `todoApi.settings` module provides the `Settings` class to manage configuration details for the Todoist API.

| Category      | Method                    | Parameters                     | Return   | Description                             |
| ------------- | ------------------------- | ------------------------------ | -------- | --------------------------------------- |
| Initialization| `Settings.__init__`       | `config_dir`: _str_ (config directory) | _None_ | Initializes the `Settings` instance    |
</details>

<details>
<summary style="font-style: italic;">
  todoApi.taskmanager
</summary>

The `todoApi.taskmanager` module provides the `TaskManager` class to manage projects, sections, and tasks in Todoist.

| Category           | Method                       | Parameters                          | Return   | Description                         |
| ------------------ | ---------------------------- | ----------------------------------- | -------- | ------------------------------------ |
| Initialization     | `TaskManager.__init__`       | `settings`: _Settings_ instance     | _None_   | Initializes the `TaskManager` instance   |
|                    |                            | `reset`: _bool_ (reset Todoist config) |        |                                      |
| Project Management | `TaskManager.project_setup`  | `semester`: _str_ (semester ID)      | _None_   | Sets up the project for the current semester |
| Section Management | `TaskManager.section_setup`  | `project_id`: _str_ (project ID)     | _None_   | Initializes sections for the project        |
| Course Management  | `TaskManager.init_courses`   | `courses`: _list_ (course list)       | _None_   | Creates labels for courses               |
| Task Management    | `TaskManager.update_assignments` | `assignments`: _list[list]_ (assignment list) | _None_ | Updates assignment tasks                  |
</details>

<details>
<summary style="font-style: italic;">
  todoApi.todoist_interfaces
</summary>

The `todoApi.todoist_interfaces` module provides the `TodoistInterface` class to interact with the Todoist API, handling projects, sections, tasks, and labels.

| Category           | Method                        | Parameters                                  | Return                 | Description                                      |
| ------------------ | ----------------------------- | ------------------------------------------- | ---------------------- | ------------------------------------------------ |
| Initialization     | `TodoistInterface.__init__`   | `settings`: _Settings_ instance             | _None_                 | Initializes the `TodoistInterface` instance      |
|                    |                              | `reset`: _bool_ (reset Todoist config)       |                        |                                                  |
| Project Management | `TodoistInterface.get_projects` | _None_                                     | _list[Project]_        | Retrieves all projects                           |
|                    | `TodoistInterface.get_project`  | `name`: _str_ (project name)                | _Optional[Project]_    | Retrieves a project by name                      |
|                    | `TodoistInterface.add_project`  | `name`: _str_ (project name)                | _Optional[Project]_    | Adds a project with the specified name           |
|                    | `TodoistInterface.favorite_project` | `project_id`: _str_ (project ID)         | _bool_                 | Favorites the specified project                  |
| Section Management | `TodoistInterface.get_sections` | `project_id`: _str_ (project ID)             | _list[Section]_        | Retrieves all sections for the specified project |
|                    | `TodoistInterface.get_section`  | `project_id`: _str_ (project ID)             | _Optional[Section]_    | Retrieves a section by name within a project     |
|                    | `TodoistInterface.add_section`  | `project_id`: _str_ (project ID)             | _Optional[Section]_    | Adds a section to the specified project          |
| Task Management    | `TodoistInterface.get_tasks`    | `project_id`: _str_ (project ID)             | _list[Task]_           | Retrieves all tasks for the specified project    |
|                    |                               | `section_id`: _str_ (section ID)             |                        |                                                  |
|                    |                               | `label`: _str_ (task label)                  |                        |                                                  |
|                    | `TodoistInterface.get_task`     | `project_id`: _str_ (project ID)             | _Optional[Task]_       | Retrieves a task by title within a project       |
|                    |                               | `title`: _str_ (task title)                  |                        |                                                  |
|                    |                               | `section_id`: _str_ (section ID)             |                        |                                                  |
|                    |                               | `label`: _str_ (task label)                  |                        |                                                  |
|                    | `TodoistInterface.add_task`     | `title`: _str_ (task title)                  | _Optional[Task]_       | Adds a task to the specified project             |
|                    |                               | `project_id`: _str_ (project ID)             |                        |                                                  |
|                    |                               | `section_id`: _str_ (section ID)             |                        |                                                  |
|                    |                               | `labels`: _list[str]_ (task labels)          |                        |                                                  |
|                    |                               | `desc`: _str_ (task description)            |                        |                                                  |
|                    |                               | `**kwargs`: additional parameters          |                        |                                                  |
|                    | `TodoistInterface.update_task`  | `task_id`: _str_ (task ID)                   | _bool_                 | Updates the task with the specified ID           |
|                    |                               | `**kwargs`: additional parameters          |                        |                                                  |
|                    | `TodoistInterface.complete_task`| `task_id`: _str_ (task ID)                   | _bool_                 | Completes the task with the specified ID         |
| Label Management   | `TodoistInterface.get_personal_labels` | _None_                              | _list[Label]_          | Retrieves all personal labels                    |
|                    | `TodoistInterface.get_label`    | `name`: _str_ (label name)                   | _Optional[Label]_      | Retrieves a label by name                        |
|                    | `TodoistInterface.add_label`    | `name`: _str_ (label name)                   | _Optional[Label]_      | Adds a label with the specified name             |
|                    |                               | `color`: _str_ (label color)                 |                        |                                                  |
</details>

</details>
