<div align="center">
    <h1>Todoist адаптер для онлайн-курсов Университета Tsinghua</h1>
    <h2>Todoist Parser for the Web Learning of Tsinghua University</h2>
    <table>
        <tr>
            <td> **中文** </td>
            <td> [English](README_en.md) </td>
            <td> [Русский](README_ru.md) </td>
        </tr>
    </table>
</div>

## Описание

Этот репозиторий представляет собой адаптер Todoist для онлайн-платформы курсов Университета Tsinghua. Он предназначен для парсинга списков курсов и домашних заданий с платформы и преобразования их в задачи Todoist.

<details>
<summary style="font-size: 1.2em; font-weight: bold;">
    Основы проекта
</summary>

#### Todoist REST API

Todoist — это инструмент для управления задачами, функционал которого в бесплатной версии сопоставим с такими инструментами, как MS To-Do. Для разработчиков Todoist предоставляет REST API, позволяющее отправлять HTTP-запросы к серверам Todoist. Также доступен Python SDK для удобной разработки на языке Python.

+ Главная страница Todoist: [https://todoist.com/](https://todoist.com/)
+ Документация Todoist REST API: [https://developer.todoist.com/rest/v2/](https://developer.todoist.com/rest/v2/)

#### euxcet/thulearn2018

Этот репозиторий — неофициальный инструмент для платформы онлайн-курсов Университета Tsinghua, предназначенный для парсинга списков курсов и домашних заданий. В данном проекте модуль `browser` обеспечивает полный функционал по парсингу, позволяя получать информацию о курсах и заданиях.

+ Репозиторий на GitHub: [![GitHub stars](https://img.shields.io/github/stars/euxcet/thulearn2018?style=social)](https://github.com/euxcet/thulearn2018)

</details>

## Структура

### Структура проекта

```plaintext
./
├── README.md
├── README_en.md
├── README_ru.md
├── src/
│   ├── main.py                     # Точка входа
│   ├── thulearn2018/               # Проект euxcet/thulearn2018
│   │   ├── __init__.py
│   │   ├── browser.py
│   │   ├── filemanager.py
│   │   ├── jsonhelper.py
│   │   ├── learn.py
│   │   ├── settings.py
│   │   ├── soup.py
│   │   └── utils.py
│   └── todoApi/                    # Обертка для Todoist API
│       ├── settings.py
│       ├── taskmanager.py
│       └── todoist_interfaces.py
└── packager/
    ├── with_console.ps1
    └── without_console.ps1
```

### Структура релизных файлов

```plaintext
Web-Learning-THU-Parser/
├── launchar.bat            # Рекомендуемый стартовый скрипт: 
│                               настраивает параметры и добавляет 
│                               задачу в Планировщик Windows
├── deleter.bat             # Удаляет задачу из Планировщика 
│                               Windows
├── with_console.exe        # Исполняемый файл с консолью
└── without_console.exe     # Исполняемый файл без консоли
```

#### `with_console.exe` и `without_console.exe`

Оба файла `with_console.exe` и `without_console.exe` являются собранными версиями `main.py` и могут быть запущены напрямую. Скрипты сборки расположены соответственно в файлах `packager/with_console.ps1` и `packager/without_console.ps1`.
+ `with_console.exe` открывает окно консоли, что позволяет настраивать параметры и просматривать журнал запуска.
+ `without_console.exe` не отображает окно консоли, поэтому при неправильной или неполной настройке возникнут ошибки.

Если при запуске `without_console.exe` возникнут ошибки, попробуйте запустить `with_console.exe` для просмотра информации об ошибке и корректировки настроек.

#### `launchar.bat`

Файл `launchar.bat` — это пакетный скрипт, который добавляет файл `without_console.exe` в Планировщик задач Windows с интервалом запуска **каждые 3 часа**. После добавления задачи запускается `with_console.exe` для первоначальной настройки параметров.

При запуске `launchar.bat` появится запрос на права администратора для добавления `without_console.exe` в Планировщик задач Windows, что обеспечивает автоматический запуск по расписанию.

#### `deleter.bat`

Файл `deleter.bat` — пакетный скрипт для удаления задачи `without_console.exe` из Планировщика Windows.

## Использование

### Прямое использование

#### 1. Регистрация в Todoist

Сначала необходимо зарегистрировать аккаунт в Todoist. Для этого перейдите на [официальный сайт Todoist](https://todoist.com/) или установите клиент Todoist.

> **Примечание**: Версия Todoist для Android доступна в Google Play. Если доступ к Google Play ограничен, попробуйте использовать [Aurora Store](https://auroraoss.com/) или скачать APK с [APKMirror](https://www.apkmirror.com/).

#### 2. Загрузка последнего релиза этого репозитория

Последнюю версию вы можете скачать со страницы [Release](https://github.com/TheTenth-THU/Web-learning-THU-parser/releases). **Скачайте zip-архив** и распакуйте его в желаемое место. **Не перемещайте, не удаляйте и не изменяйте файлы внутри распакованной папки**.

#### 3. Запуск `launchar.bat`

В распакованной папке дважды кликните на `launchar.bat`. При этом появится запрос на права администратора для добавления задачи `without_console.exe` в Планировщик Windows, что обеспечит её периодический запуск.

После подтверждения прав, откроется окно консоли через `with_console.exe`, в котором вы сможете ввести Todoist API Token, указать путь для сохранения конфигурации, а также задать имя пользователя и пароль для доступа к онлайн-платформе.

### Для разработчиков

В данном проекте внесены изменения в оригинальный код проекта euxcet/thulearn2018, с добавлением обширных docstring-комментариев для облегчения дальнейшей разработки. Также реализована обертка для Todoist REST API для удобства разработчиков.

#### Зависимости

Требуется Python версии:
+ **3.7 и выше**, для поддержки новых возможностей SSL.
+ **до 3.9**, для гарантии совместимости при повторном рукопожатии SSL.

Среда для разработки и тестирования проекта — **Python 3.9.13**. Вы можете использовать такие инструменты, как Anaconda или [pyenv](https://github.com/pyenv/pyenv) (на Windows: [pyenv-win](https://github.com/pyenv-win/pyenv-win)) для создания виртуального окружения с подходящей версией Python.

Для установки зависимостей выполните команду:

```shell
pip install -r requirements.txt
```

#### Обзор модулей

<details>
<summary style="font-weight: bold;">
    thulearn2018/
</summary>

<details>
<summary style="font-style: italic;">
    `thulearn2018.settings`
</summary>

Модуль `thulearn2018.settings` предоставляет класс `Settings` для управления параметрами конфигурации.

| Категория     | Метод                   | Параметры                 | Возвращаемое значение | Описание                              |
|---------------|-------------------------|---------------------------|-----------------------|---------------------------------------|
| Инициализация | `Settings.__init__`     | `path`: _str_ – путь к файлу конфигурации | _None_           | Инициализация класса `Settings`       |

</details>

<details>
<summary style="font-style: italic;">
    `thulearn2018.browser`
</summary>

Модуль `thulearn2018.browser` интегрирует функции для парсинга списков курсов и домашних заданий онлайн-платформы, предоставляя класс `Learn`.

| Категория        | Метод                     | Параметры                        | Возвращаемое значение | Описание                                |
|------------------|---------------------------|----------------------------------|-----------------------|-----------------------------------------|
| Инициализация    | `Learn.__init__`          | `settings`: экземпляр класса `Settings`  | _None_           | Инициализация класса `Learn`            |
|                  |                           | `reset`: _bool_ – ввод заново логина и пароля |                   |                                         |
| Управление пользователем | `Learn.set_user`   | _void_                           | _None_                | Установка имени пользователя и пароля   |
|                  | `Learn.get_user`          | _void_                           | _str_                 | Получение текущего имени пользователя и пароля |
| Файловое управление | `Learn.set_path`       | _void_                           | _None_                | Установка пути для сохранения файлов    |
|                  | `Learn.get_path`          | _void_                           | _str_                 | Получение текущего пути для сохранения    |
|                  | `Learn.set_local`         | _void_                           | _None_                | Сброс (очистка) локальной записи        |
| Управление подключением | `Learn.login`       | `mode`: _str_ – режим входа в систему | _None_            | Вход на платформу с использованием логина и пароля |
| Управление курсами | `Learn.set_semester`    | `semester`: _str_ – идентификатор семестра | _None_           | Установка текущего семестра             |
|                  | `Learn.get_lessons`       | `exclude`: _list_ – список курсов для исключения | _list_           | Получение списка курсов текущего семестра |
|                  |                           | `include`: _list_ – список курсов для включения |                   |                                         |
|                  | `Learn.init_lessons`      | `exclude`: _list_ – список курсов для исключения | _list_           | Создание директорий для курсов          |
|                  |                           | `include`: _list_ – список курсов для включения |                   |                                         |
| Управление заданиями | `Learn.get_files_id`  | `lesson_id`: _str_ – идентификатор курса | _list_           | Получение списка идентификаторов файлов курса |
|                  | `Learn.file_id_exist`     | `fid`: _str_ – идентификатор файла | _bool_                 | Проверка наличия идентификатора файла локально |
|                  | `Learn.save_file_id`      | `fid`: _str_ – идентификатор файла | _None_                | Сохранение идентификатора файла локально |
|                  | `Learn.download_files`    | `lesson_id`: _str_ – идентификатор курса | _None_            | Загрузка файлов курса                   |
|                  |                           | `lesson_name`: _str_ – название курса |                   |                                         |
|                  |                           | `file_id`: _str_ – идентификатор файла |                   |                                         |
|                  | `Learn.download_homework` | `lesson_id`: _str_ – идентификатор курса | _list_           | Загрузка домашних заданий курса         |
|                  |                           | `lesson_name`: _str_ – название курса |                   |                                         |
|                  |                           | `download_submission`: _bool_ – скачивать ли отправленные задания | |                                         |
|                  |                           | `download_files`: _bool_ – скачивать ли файлы |                   |                                         |
|                  | `Learn.upload`            | `homework_id`: _str_ – идентификатор задания | _None_           | Загрузка файлов для выполнения задания  |
|                  |                           | `file_path`: _str_ – путь к файлу |                   |                                         |
|                  |                           | `message`: _str_ – информация о загрузке |                   |                                         |
|                  | `Learn.get_ddl`           | `lessons`: _list_ – список курсов | _list_                | Получение списка сроков сдачи домашних заданий |
|                  |                           | `download_submission`: _bool_ – скачивать ли отправленные задания | |                                         |
|                  |                           | `download_files`: _bool_ – скачивать ли файлы |                   |                                         |

</details>

<details>
<summary style="font-style: italic;">
    `thulearn2018.learn`
</summary>

Модуль `thulearn2018.learn` реализует интерфейс командной строки (CLI) для взаимодействия с онлайн-платформой Университета Tsinghua с использованием библиотеки `click`. Он предоставляет следующие команды:
 
| Категория         | Команда        | Параметры                              | Возвращаемое значение | Описание                                |
|-------------------|----------------|----------------------------------------|-----------------------|-----------------------------------------|
| Загрузка          | `download`     | `exclude`: _str_ – список курсов для исключения | _None_        | Загрузка всех файлов для выбранных курсов и семестра |
|                   |                | `include`: _str_ – список курсов для включения |                   |                                         |
|                   |                | `semester`: _str_ – идентификатор семестра |                   |                                         |
|                   |                | `path`: _str_ – путь для сохранения файлов |                   |                                         |
|                   |                | `download_submission`: _bool_ – скачивать ли выполненные задания | |                                         |
| Сброс конфигурации| `reset`        | _void_                                 | _None_                | Сброс параметров, например, имени пользователя и пути сохранения |
| Просмотр настроек | `config`       | _void_                                 | _None_                | Отображение текущих настроек (например, имя пользователя и путь) |
| Очистка записей   | `clear`        | `semester`: _str_ – идентификатор семестра | _None_             | Очистка всех записей загрузок для указанного семестра |
| Отправка задания  | `submit`       | `name`: _str_ – путь к файлу задания    | _None_                | Отправка файла задания с указанной информацией |
|                   |                | `m`: _str_ – информация о задании        |                     |                                         |
| Сроки сдачи       | `ddl`          | `exclude`: _str_ – список курсов для исключения | _None_         | Отображение сроков сдачи для выбранных курсов и семестра |
|                   |                | `include`: _str_ – список курсов для включения |                   |                                         |
|                   |                | `semester`: _str_ – идентификатор семестра |                   |                                         |
|                   |                | `path`: _str_ – путь для сохранения файлов задания |                  |                                         |
|                   |                | `download_submission`: _bool_ – скачивать ли выполненные задания |             |                                         |

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

Модуль `todoApi.settings` предоставляет класс `Settings` для управления параметрами конфигурации Todoist API.

| Категория     | Метод                   | Параметры                      | Возвращаемое значение | Описание                               |
|---------------|-------------------------|--------------------------------|-----------------------|----------------------------------------|
| Инициализация | `Settings.__init__`     | `config_dir`: _str_ – каталог с конфигурационными файлами | _None_           | Инициализация класса `Settings`         |

</details>

<details>
<summary style="font-style: italic;">
    `todoApi.taskmanager`
</summary>

Модуль `todoApi.taskmanager` предоставляет класс `TaskManager` для управления проектами, секциями и задачами в Todoist.

| Категория         | Метод                        | Параметры                      | Возвращаемое значение | Описание                                |
|-------------------|------------------------------|--------------------------------|-----------------------|-----------------------------------------|
| Инициализация     | `TaskManager.__init__`       | `settings`: экземпляр класса `Settings` | _None_          | Инициализация класса `TaskManager`      |
|                   |                              | `reset`: _bool_ – сброс конфигурации Todoist |                   |                                         |
| Управление проектами | `TaskManager.project_setup` | `semester`: _str_ – идентификатор семестра | _None_          | Настройка проекта для текущего семестра |
| Управление секциями  | `TaskManager.section_setup` | `project_id`: _str_ – идентификатор проекта | _None_        | Инициализация секций проекта            |
| Управление курсами | `TaskManager.init_courses`  | `courses`: _list_ – список курсов | _None_              | Создание меток для курсов               |
| Управление задачами | `TaskManager.update_assignments` | `assignments`: _list[list]_ – список заданий | _None_         | Обновление задач по домашним заданиям   |

</details>

<details>
<summary style="font-style: italic;">
    `todoApi.todoist_interfaces`
</summary>

Модуль `todoApi.todoist_interfaces` предоставляет класс `TodoistInterface` для взаимодействия с Todoist API, управления проектами, секциями, задачами и метками.

| Категория         | Метод                        | Параметры                              | Возвращаемое значение | Описание                                |
|-------------------|------------------------------|----------------------------------------|-----------------------|-----------------------------------------|
| Инициализация     | `TodoistInterface.__init__`  | `settings`: экземпляр класса `Settings`| _None_                | Инициализация класса `TodoistInterface` |
|                   |                              | `reset`: _bool_ – сброс конфигурации Todoist |                   |                                         |
| Управление проектами | `TodoistInterface.get_projects` | _void_                           | _list[Project]_       | Получение списка всех проектов          |
|                   | `TodoistInterface.get_project`  | `name`: _str_ – имя проекта             | _Optional[Project]_   | Получение проекта по имени              |
|                   | `TodoistInterface.add_project`  | `name`: _str_ – имя проекта             | _Optional[Project]_   | Добавление проекта с указанным именем   |
|                   | `TodoistInterface.favorite_project` | `project_id`: _str_ – идентификатор проекта | _bool_           | Добавление проекта в избранное          |
| Управление секциями  | `TodoistInterface.get_sections` | `project_id`: _str_ – идентификатор проекта | _list[Section]_  | Получение списка секций проекта         |
|                   | `TodoistInterface.get_section`  | `project_id`: _str_ – идентификатор проекта | _Optional[Section]_ | Получение определённой секции проекта     |
|                   | `TodoistInterface.add_section`  | `project_id`: _str_ – идентификатор проекта | _Optional[Section]_ | Добавление секции в проект              |
| Управление задачами  | `TodoistInterface.get_tasks`   | `project_id`: _str_ – идентификатор проекта | _list[Task]_       | Получение всех задач проекта            |
|                   |                               | `section_id`: _str_ – идентификатор секции |                     |                                         |
|                   |                               | `label`: _str_ – метка задачи             |                     |                                         |
|                   | `TodoistInterface.get_task`    | `project_id`: _str_ – идентификатор проекта | _Optional[Task]_   | Получение задачи с определённым заголовком в проекте |
|                   |                               | `title`: _str_ – заголовок задачи          |                     |                                         |
|                   |                               | `section_id`: _str_ – идентификатор секции |                     |                                         |
|                   |                               | `label`: _str_ – метка задачи             |                     |                                         |
|                   | `TodoistInterface.add_task`    | `title`: _str_ – заголовок задачи          | _Optional[Task]_   | Добавление задачи в проект              |
|                   |                               | `project_id`: _str_ – идентификатор проекта |                     |                                         |
|                   |                               | `section_id`: _str_ – идентификатор секции |                     |                                         |
|                   |                               | `labels`: _list[str]_ – список меток        |                     |                                         |
|                   |                               | `desc`: _str_ – описание задачи            |                     |                                         |
|                   |                               | `**kwargs`: дополнительные параметры       |                     |                                         |
|                   | `TodoistInterface.update_task` | `task_id`: _str_ – идентификатор задачи     | _bool_                | Обновление задачи по идентификатору     |
|                   |                               | `**kwargs`: дополнительные параметры       |                     |                                         |
|                   | `TodoistInterface.complete_task` | `task_id`: _str_ – идентификатор задачи   | _bool_                | Завершение задачи по идентификатору       |
| Управление метками  | `TodoistInterface.get_personal_labels` | _void_                      | _list[Label]_        | Получение списка всех личных меток       |
|                   | `TodoistInterface.get_label`   | `name`: _str_ – имя метки                  | _Optional[Label]_  | Получение метки по имени                |
|                   | `TodoistInterface.add_label`   | `name`: _str_ – имя метки                  | _Optional[Label]_  | Добавление метки с указанным именем       |
|                   |                               | `color`: _str_ – цвет метки                |                     |                                         |

</details>

</details>