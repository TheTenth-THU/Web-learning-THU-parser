<div align="center">
    <h1>针对华清大学网络学堂的 Todoist 适配工具</h1>
    <h2>Todoist Parser for the Web Learning of Tsinghua University</h2>
    <table><tr>
        <td style="font-weight: bold">中文</td>
        <td><a href="README_en.md">English</a></td>
        <td><a href="README_ru.md">Русский</a></td>
    </tr></table>
</div>

## 介绍

此仓库是一个针对华清大学网络学堂的 Todoist 适配工具，用于解析网络学堂的课程列表和作业列表，并将其转换为 Todoist 任务。

<details>
<summary style="font-size: 1.2em; font-weight: bold;">
    项目基础
</summary>

#### Todoist REST API

Todoist 是一款待办任务管理工具，其免费版提供的功能即与 MS To-Do 等工具相当。Todoist 面向开发者提供了 REST API，允许开发者通过 HTTP 请求与 Todoist 服务器进行交互；同时，Todoist 也提供了 Python SDK，方便开发者使用 Python 语言进行开发。

+ Todoist 首页：[https://todoist.com/](https://todoist.com/)
+ Todoist REST API 文档：[https://developer.todoist.com/rest/v2/](https://developer.todoist.com/rest/v2/)

#### euxcet/thulearn2018

此仓库是一个针对华清大学网络学堂的非官方工具，用于解析网络学堂的课程列表和作业列表。该项目中 `browser` 模块提供了解析网络学堂的完整功能，可以用于获取课程列表、作业列表等信息。

+ GitHub 仓库：[![GitHub stars](https://img.shields.io/github/stars/euxcet/thulearn2018?style=social)](https://github.com/euxcet/thulearn2018)

</details>

## 结构

### 项目结构

```plaintext
./
├── README.md
├── README_en.md
├── README_ru.md
├── src/
│   ├── main.py                     # 入口
│   ├── thulearn2018/               # euxcet/thulearn2018 项目
│   │   ├── __init__.py
│   │   ├── browser.py
│   │   ├── filemanager.py
│   │   ├── jsonhelper.py
│   │   ├── learn.py
│   │   ├── settings.py
│   │   ├── soup.py
│   │   └── utils.py
│   └── todoApi/                    # Todoist API 包装
│       ├── settings.py
│       ├── taskmanager.py
│       └── todoist_interfaces.py
└── packager/
    ├── with_console.ps1
    └── without_console.ps1
```

### 发布文件结构

```plaintext
Web-Learning-THU-Parser/
├── launchar.bat            # 推荐启动入口，配置信息并添加定时任务
├── deleter.bat             # 删除定时任务
├── with_console.exe        # 带控制台的可执行文件
└── without_console.exe     # 无控制台的可执行文件
```

#### `with_console.exe` 和 `without_console.exe`

`with_console.exe` 和 `without_console.exe` 均为 `main.py` 的打包文件，均可直接运行。对应的打包脚本分别为 `packager/with_console.ps1` 和 `packager/without_console.ps1`。
+ `with_console.exe` 会打开控制台窗口，因此可以配置信息并查看运行日志。
+ `without_console.exe` 不会打开控制台窗口，因此无法查看运行日志，如果配置信息不全或有误将报错。

如果运行 `without_console.exe` 时报错，请尝试运行 `with_console.exe`，查看报错信息或补全配置信息。

#### `launchar.bat`

`launchar.bat` 是一个批处理文件，将 `without_console.exe` 添加到 Windows 定时任务中，**每 3 小时**运行一次；同时，其会在添加定时任务后运行 `with_console.exe`，以进行信息配置。

双击运行 `launchar.bat` 时，会弹出窗口要求管理员权限，以将 `without_console.exe` 添加到 Windows 定时任务中，实现定时运行。

#### `deleter.bat`

`deleter.bat` 是一个批处理文件，用于删除 Windows 定时任务中的 `without_console.exe`。

## 使用

### 直接使用

#### 1. 注册 Todoist

首先，您需要注册一个 Todoist 账号。您可以通过 [Todoist 官网](https://todoist.com/)注册账号，或者下载 Todoist 客户端。

> **注**：Todoist for Android 需要从 Google Play 商店下载。如果您无法访问 Google Play 商店，请尝试使用 [Aurora Store](https://auroraoss.com/)，或者从 [APKMirror](https://www.apkmirror.com/) 下载 Todoist 的 APK 文件。

#### 2. 下载本仓库的最新 Release

您可以在本仓库的 [Release 页面](https://github.com/TheTenth-THU/Web-learning-THU-parser/releases)下载最新的 Release。**只需下载 zip 文件**，并解压到期望位置。**请勿移动、删除或修改解压后文件夹中的任何文件**。

#### 3. 运行 `launchar.bat`

在解压后的文件夹中，双击运行 `launchar.bat`。其会弹出窗口**要求管理员权限**，以将 `without_console.exe` 添加到 Windows 定时任务中，实现定时运行。

授予管理员权限后，`with_console.exe` 会打开控制台窗口，您可以根据提示输入 Todoist API Token、配置文件保存路径、网络学堂用户名和密码等信息。

### 自行开发

本项目修改了 euxcet/thulearn2018 项目的部分代码，同时**添加了大量 docstring 注释**，可能会开发有所帮助；同时，本项目也添加了对 Todoist REST API 的封装，方便开发者使用。

#### 配置依赖

本项目要求 Python 版本为：
+ **3.7 以上**，以支持新的 SSL 重协商特性。
+ **3.9 及以下**，以在 SSL 重协商中保证兼容性。

项目的开发测试环境为 **Python 3.9.13**。您可以使用 Anaconda 等工具，或者使用 [pyenv](https://github.com/pyenv/pyenv)（Windows 下 [pyevn-win](https://github.com/pyenv-win/pyenv-win)）等模块创建版本符合要求的虚拟环境。

您可以使用以下命令安装项目的依赖：

```shell
pip install -r requirements.txt
```

#### 模块说明

<details>
<summary style="font-weight: bold;">
    thulearn2018/
</summary>

<details>
<summary style="font-style: italic;">
    `thulearn2018.settings`
</summary>

本仓库 `thulearn2018.settings` 模块提供了 `Settings` 类，用于管理配置信息。

| 分类 | 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- | --- |
| 初始化 | `Settings.__init__` | `path`: _str_，配置文件路径 | _None_ | 初始化 `Settings` 类 |

</details>

<details>
<summary style="font-style: italic;">
    `thulearn2018.browser`
</summary>

本仓库 `thulearn2018.browser` 模块集成了**解析网络学堂的课程列表、作业列表**等功能，提供了 `Learn` 类来实现这些功能。

| 分类 | 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- | --- |
| 初始化 | `Learn.__init__` | `settings`: _Settings_ 类实例 | _None_ | 初始化 `Learn` 类 |
| ^^ | ^^ | `reset`: _bool_，是否重新输入用户名和密码 | ^^ | ^^ |
| 用户管理 | `Learn.set_user` | _void_ | _None_ | 设置网络学堂用户名和密码 |
| ^^ | `Learn.get_user` | _void_ | _str_ | 获取当前用户名和密码 |
| 文件管理 | `Learn.set_path` | _void_ | _None_ | 设置保存文件的路径 |
| ^^ | `Learn.get_path` | _void_ | _str_ | 获取当前保存文件的路径 |
| ^^ | `Learn.set_local` | _void_ | _None_ | 重置（清除）文件记录 |
| 网络连接管理 | `Learn.login` | `mode`: _str_，登录模式 | _None_ | 使用用户名和密码登录平台 |
| 课程管理 | `Learn.set_semester` | `semester`: _str_，学期 ID | _None_ | 设置当前学期 |
| ^^ | `Learn.get_lessons` | `exclude`: _list_，排除的课程名列表 | _list_ | 获取当前学期的课程列表 |
| ^^ | ^^ | `include`: _list_，包含的课程名列表 | ^^ | ^^ |
| ^^ | `Learn.init_lessons` | `exclude`: _list_，排除的课程名列表 | _list_ | 为课程创建目录 |
| ^^ | ^^ | `include`: _list_，包含的课程名列表 | ^^ | ^^ |
| 任务管理 | `Learn.get_files_id` | `lesson_id`: _str_，课程 ID | _list_ | 获取课程的文件 ID 列表 |
| ^^ | `Learn.file_id_exist` | `fid`: _str_，文件 ID | _bool_ | 检查文件 ID 是否存在于本地文件 |
| ^^ | `Learn.save_file_id` | `fid`: _str_，文件 ID | _None_ | 将文件 ID 保存到本地文件 |
| ^^ | `Learn.download_files` | `lesson_id`: _str_，课程 ID | _None_ | 下载课程的文件 |
| ^^ | ^^ | `lesson_name`: _str_，课程名 | ^^ | ^^ |
| ^^ | ^^ | `file_id`: _str_，文件 ID | ^^ | ^^ |
| ^^ | `Learn.download_homework` | `lesson_id`: _str_，课程 ID | _list_ | 下载课程的作业 |
| ^^ | ^^ | `lesson_name`: _str_，课程名 | ^^ | ^^ |
| ^^ | ^^ | `download_submission`: _bool_，是否下载提交的作业 | ^^ | ^^ |
| ^^ | ^^ | `download_files`: _bool_，是否下载文件 | ^^ | ^^ |
| ^^ | `Learn.upload` | `homework_id`: _str_，作业 ID | _None_ | 上传作业文件 |
| ^^ | ^^ | `file_path`: _str_，文件路径 | ^^ | ^^ |
| ^^ | ^^ | `message`: _str_，上传信息 | ^^ | ^^ |
| ^^ | `Learn.get_ddl` | `lessons`: _list_，课程列表 | _list_ | 获取课程的作业截止日期列表 |
| ^^ | ^^ | `download_submission`: _bool_，是否下载提交的作业 | ^^ | ^^ |
| ^^ | ^^ | `download_files`: _bool_，是否下载文件 | ^^ | ^^ |

</details>

<details>
<summary style="font-style: italic;">
    `thulearn2018.learn`
</summary>

本仓库 `thulearn2018.learn` 模块提供了命令行接口（CLI），用于与华清大学网络学堂进行交互。该模块使用 `click` 库实现了多个命令，包括下载课程文件、重置配置、显示配置、清除下载记录、提交作业和显示作业截止日期。

| 分类 | 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- | --- |
| 下载 | `download` | `exclude`: _str_，排除的课程名列表 | _None_ | 下载指定课程和学期的所有课程文件 |
| ^^ | ^^ | `include`: _str_，包含的课程名列表 | ^^ | ^^ |
| ^^ | ^^ | `semester`: _str_，学期 ID | ^^ | ^^ |
| ^^ | ^^ | `path`: _str_，保存文件的路径 | ^^ | ^^ |
| ^^ | ^^ | `download_submission`: _bool_，是否下载提交的作业 | ^^ | ^^ |
| 重置 | `reset` | _void_ | _None_ | 重置配置，如用户名和路径 |
| 显示配置 | `config` | _void_ | _None_ | 显示当前配置，包括用户名和路径 |
| 清除记录 | `clear` | `semester`: _str_，学期 ID | _None_ | 清除指定学期的所有下载记录 |
| 提交作业 | `submit` | `name`: _str_，作业文件路径 | _None_ | 提交指定名称和信息的作业 |
| ^^ | ^^ | `m`: _str_，提交信息 | ^^ | ^^ |
| 显示截止日期 | `ddl` | `exclude`: _str_，排除的课程名列表 | _None_ | 显示指定课程和学期的作业截止日期 |
| ^^ | ^^ | `include`: _str_，包含的课程名列表 | ^^ | ^^ |
| ^^ | ^^ | `semester`: _str_，学期 ID | ^^ | ^^ |
| ^^ | ^^ | `path`: _str_，保存作业文件的路径 | ^^ | ^^ |
| ^^ | ^^ | `download_submission`: _bool_，是否下载提交的作业 | ^^ | ^^ |

</details>
</details>

<details>
<summary style="font-weight: bold;">
    todoApi/
</summary>

<details>
<summary style="font-style: italic;">
    `todoApi.settings`
</summary>

本仓库 `todoApi.settings` 模块提供了 `Settings` 类，用于管理 Todoist API 的配置信息。

| 分类 | 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- | --- |
| 初始化 | `Settings.__init__` | `config_dir`: _str_，配置文件目录 | _None_ | 初始化 `Settings` 类 |

</details>

<details>
<summary style="font-style: italic;">
    `todoApi.taskmanager`
</summary>

本仓库 `todoApi.taskmanager` 模块提供了 `TaskManager` 类，用于管理 Todoist 中的项目、章节和任务。

| 分类 | 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- | --- |
| 初始化 | `TaskManager.__init__` | `settings`: _Settings_ 类实例 | _None_ | 初始化 `TaskManager` 类 |
| ^^ | ^^ | `reset`: _bool_，是否重置 Todoist 配置 | ^^ | ^^ |
| 项目管理 | `TaskManager.project_setup` | `semester`: _str_，学期 ID | _None_ | 设置当前学期项目 |
| 章节管理 | `TaskManager.section_setup` | `project_id`: _str_，项目 ID | _None_ | 初始化项目章节 |
| 课程管理 | `TaskManager.init_courses` | `courses`: _list_，课程列表 | _None_ | 创建课程标签 |
| 任务管理 | `TaskManager.update_assignments` | `assignments`: _list[list]_，作业列表 | _None_ | 更新作业任务 |

</details>

<details>
<summary style="font-style: italic;">
    `todoApi.todoist_interfaces`
</summary>

本仓库 `todoApi.todoist_interfaces` 模块提供了 `TodoistInterface` 类，用于与 Todoist API 进行交互，管理项目、章节、任务和标签。

| 分类 | 方法 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- | --- |
| 初始化 | `TodoistInterface.__init__` | `settings`: _Settings_ 类实例 | _None_ | 初始化 `TodoistInterface` 类 |
| ^^ | ^^ | `reset`: _bool_，是否重置 Todoist 配置 | ^^ | ^^ |
| 项目管理 | `TodoistInterface.get_projects` | _void_ | _list[Project]_ | 获取所有项目 |
| ^^ | `TodoistInterface.get_project` | `name`: _str_，项目名称 | _Optional[Project]_ | 获取指定名称的项目 |
| ^^ | `TodoistInterface.add_project` | `name`: _str_，项目名称 | _Optional[Project]_ | 添加指定名称的项目 |
| ^^ | `TodoistInterface.favorite_project` | `project_id`: _str_，项目 ID | _bool_ | 收藏指定 ID 的项目 |
| 章节管理 | `TodoistInterface.get_sections` | `project_id`: _str_，项目 ID | _list[Section]_ | 获取指定项目的所有章节 |
| ^^ | `TodoistInterface.get_section` | `project_id`: _str_，项目 ID | _Optional[Section]_ | 获取指定项目中指定名称的章节 |
| ^^ | `TodoistInterface.add_section` | `project_id`: _str_，项目 ID | _Optional[Section]_ | 添加指定名称的章节到指定项目 |
| 任务管理 | `TodoistInterface.get_tasks` | `project_id`: _str_，项目 ID | _list[Task]_ | 获取指定项目的所有任务 |
| ^^ | ^^ | `section_id`: _str_，章节 ID | ^^ | ^^ |
| ^^ | ^^ | `label`: _str_，任务标签 | ^^ | ^^ |
| ^^ | `TodoistInterface.get_task` | `project_id`: _str_，项目 ID | _Optional[Task]_ | 获取指定项目中指定标题的任务 |
| ^^ | ^^ | `title`: _str_，任务标题 | ^^ | ^^ |
| ^^ | ^^ | `section_id`: _str_，章节 ID | ^^ | ^^ |
| ^^ | ^^ | `label`: _str_，任务标签 | ^^ | ^^ |
| ^^ | `TodoistInterface.add_task` | `title`: _str_，任务标题 | _Optional[Task]_ | 添加任务到指定项目 |
| ^^ | ^^ | `project_id`: _str_，项目 ID | ^^ | ^^ |
| ^^ | ^^ | `section_id`: _str_，章节 ID | ^^ | ^^ |
| ^^ | ^^ | `labels`: _list[str]_，任务标签 | ^^ | ^^ |
| ^^ | ^^ | `desc`: _str_，任务描述 | ^^ | ^^ |
| ^^ | ^^ | `**kwargs`: 其他参数 | ^^ | ^^ |
| ^^ | `TodoistInterface.update_task` | `task_id`: _str_，任务 ID | _bool_ | 更新指定 ID 的任务 |
| ^^ | ^^ | `**kwargs`: 其他参数 | ^^ | ^^ |
| ^^ | `TodoistInterface.complete_task` | `task_id`: _str_，任务 ID | _bool_ | 完成指定 ID 的任务 |
| 标签管理 | `TodoistInterface.get_personal_labels` | _void_ | _list[Label]_ | 获取所有个人标签 |
| ^^ | `TodoistInterface.get_label` | `name`: _str_，标签名称 | _Optional[Label]_ | 获取指定名称的标签 |
| ^^ | `TodoistInterface.add_label` | `name`: _str_，标签名称 | _Optional[Label]_ | 添加指定名称的标签 |
| ^^ | ^^ | `color`: _str_，标签颜色 | ^^ | ^^ |

</details>

</details>