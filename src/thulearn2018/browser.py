""" Provides the `Learn` class for interacting with the Tsinghua Web Learning 2018 platform. 

This script provides a class for interacting with the Web Learning. Methods in this class use the `requests` library to send HTTP requests to the platform, and use the `BeautifulSoup` library to parse the HTML content.

## Methods

### User management

    **set_user** (_void_) -> _None_
    Call `FileManager.set_user()` to set the username and password.
    **get_user** (_void_) -> _str_
    Call `FileManager.get_user()` to get current username and password.

### File management

    **set_path** (_void_) -> _None_
    Call `FileManager.set_path()` to set the path to save files.
    **get_path** (_void_) -> _str_
    Call `FileManager.get_path()` to get current path to save files.
    **set_local** (_void_) -> _None_
    Call `FileManager.set_local()` to reset (clear) the file record.

### Web connection management
    
    **login** (_void_) -> _None_
    Log in to the platform using the username and password.

### Course management

    **set_semester** (_str_) -> _None_
    Set the current semester.
    **get_lessons** (_list_) -> _list_
    Get the list of lessons for the current semester.
    **init_lessons** (_list_) -> _list_
    Make directories for the lessons.

### Task management

    **get_files_id** (_str_) -> _list_
    Get the list of file IDs for a lesson.
    **file_id_exist** (_str_) -> _bool_
    Check if a file ID exists in the local file.
    **save_file_id** (_str_) -> _None_
    Save the file ID to the local file.
    **download_files** (_str_) -> _None_
    Download files for a lesson.
    **download_homework** (_str_) -> _list_
    Download homework for a lesson.
    **upload** (_str_) -> _None_
    Upload a file for a homework assignment.
    **get_ddl** (_list_) -> _list_
    Get the list of homework deadlines for the lessons.
"""

import os
import sys
import ssl
import requests
from urllib.parse import quote
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

from . import filemanager, jsonhelper, soup, utils
from .settings import Settings

ssl._create_default_https_context = ssl._create_unverified_context

# class SSLAdapter(requests.adapters.HTTPAdapter):
#     def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
#         ctx = ssl.create_default_context()
#         # 禁用证书验证（注意安全风险）
#         ctx.check_hostname = False
#         ctx.verify_mode = ssl.CERT_NONE
#         ctx.set_ciphers("DEFAULT@SECLEVEL=1")
#         ctx.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0)
#         kwargs['ssl_context'] = ctx
#         return super(SSLAdapter, self).init_poolmanager(connections, maxsize, block, **kwargs)
    
#     def proxy_manager_for(self, proxy, **kwargs):
#         ctx = ssl.create_default_context()
#         ctx.check_hostname = False
#         ctx.verify_mode = ssl.CERT_NONE
#         ctx.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0)
#         kwargs['ssl_context'] = ctx
#         return super(SSLAdapter, self).proxy_manager_for(proxy, **kwargs)

class Learn():
    def __init__(self, settings: Settings, reset=False):
        """Initialize the `Learn` class.
        
        This method initializes the `Learn` class by setting up the session and headers for the `requests` library, and creating instances of the `FileManager`, `JsonHelper` and `Soup` classes.
        """
        self.settings = settings

        # disable_warnings(InsecureRequestWarning)
        self.session = requests.Session()
        # self.session.mount('https://', SSLAdapter())
        self.session.headers = self.settings.headers

        self.fm = filemanager.FileManager(self.settings)
        self.reset = reset
        if self.reset:
            self.fm.set_user()
            self.fm.set_path()
        self.username, self.password = self.fm.get_user()
        self.path = self.fm.get_path()

        self.soup = soup.Soup(self.settings)
        self.jh = jsonhelper.JsonHelper()

    def set_user(self):
        """Call `FileManager.set_user()` to set the username and password."""
        self.fm.set_user()

    def set_path(self):
        """Call `FileManager.set_path()` to set the path to save files."""
        self.fm.set_path()

    def set_local(self):
        """Call `FileManager.set_local()` to reset (clear) the file record."""
        self.fm.set_local()

    def get_path(self):
        """Call `FileManager.get_path()` to get current path to save files."""
        return self.fm.get_path()

    def get_user(self):
        """Call `FileManager.get_user()` to get current username and password."""
        return self.fm.get_user()

    def _post(self, url, form={}, csrf=True, headers=None):
        """(internal) Send a POST request to the platform.
        
        The POST request is sent to the specified URL with the form data. If the `csrf` parameter is set to `True`, the CSRF token is included in the request. The `headers` parameter can be used to specify additional headers for the request.
        
        Args:
            url (str):          The URL to send the request to.
            form (dict):        The form data to include in the request.
            csrf (bool):        Whether to include the CSRF token in the request.
            headers (dict):     Additional headers to include in the request.
        """
        if csrf:
            params = {
                '_csrf': self.session.cookies.get_dict()['XSRF-TOKEN']
            }
            return self.session.post(url, data=form, params=params, #verify=False,
                                     headers=headers).content
        else:
            self.session.trust_env = False
            return self.session.post(url, data=form, #verify=False,
                                     headers=headers).content

    def _get(self, url, params={}, csrf=True, headers={}):
        """(internal) Send a GET request to the platform.

        The GET request is sent to the specified URL with the query parameters. If the `csrf` parameter is set to `True`, the CSRF token is included in the request.

        Args:
            url (str):          The URL to send the request to.
            params (dict):      The query parameters to include in the request.
            csrf (bool):        Whether to include the CSRF token in the request.
        """
        if csrf:
            params.update({
                '_csrf': self.session.cookies.get_dict()['XSRF-TOKEN']
            })
        headers.update(self.settings.headers)
        return self.session.get(url, params=params).content

    def login(self, mode="init"):
        """Log in to the platform using the username and password."""
        if mode == "init":
            form = {"i_user": self.username, "i_pass": self.password}
            content = self._post(self.settings.login_id_url, form, csrf=False)
            ticket = self.soup.parse_ticket(content)
            self._post(self.settings.login_url + ticket, csrf=False)
        elif mode == "keep":
            print("To keep login status, please input the `ticket` for the current session:")
            ticket = input()
            self._post(self.settings.login_url + '/?' + f'ticket={ticket}', csrf=False)

    def set_semester(self, semester=""):
        """Set the current semester.

        If the semester is not specified, the current semester is determined by sending a request to the platform. The semester ID is then stored in the `semester` attribute of the class. The local file is then created or redirected to the current semester.

        Args:
            semester (str):     The semester ID, e.g. "2023-2024-1".
        """
        if semester != "":
            self.semester = semester
        else:
            content = self.jh.loads(self._get(self.settings.semester_url))
            self.semester = content["result"]["id"]
            semester_file_path = os.path.join(
                self.settings.config_dir, self.semester+".txt")
            if os.path.exists(self.settings.local_file_path) and \
               not os.path.islink(self.settings.local_file_path):
                os.rename(self.settings.local_file_path,
                          semester_file_path)
        # create or redirect local.txt to current semester
        if not os.path.exists(semester_file_path):
            with open(semester_file_path, 'w') as f:
                pass
        if os.path.exists(self.settings.local_file_path):
            os.unlink(self.settings.local_file_path)
        if os.name == 'nt':
            os.link(semester_file_path, self.settings.local_file_path)
        else:
            os.symlink(semester_file_path, self.settings.local_file_path)
        self.local = self.fm.get_local()
        return self.semester

    # -------------------------------------------------------------------------
    def get_lessons(self, exclude=[], include=[]):
        """Get the list of lessons for the current semester.

        This method sends a request to the platform to get the list of lessons for the current semester. The list is then sorted by **lesson name** ("kcm") and **teacher name** ("jsm"). 

        If there are multiple lessons with the same name, the **folder name** is determined based on the previous and next lessons:
        + The folder name is set to **lesson name**, if the lesson is unique,
        + The folder name is set to **lesson name_teacher name**, if the lesson has the same name but different teachers,
        + The folder name is set to **lesson name_course code**, if the lesson has the same name and teacher but different course codes ("kch").

        Args:
            exclude (list):         List of lesson names to exclude.
            include (list):         List of lesson names to include. If specified, only lessons with names in this list will be included.

        Returns:
            lessons (list):         List of lessons, each represented as a list of the form [_lesson_id_, _lesson_name_, _teacher_name_, _course_code_, _folder_name_].
        """
        content = self.jh.loads(self._post(self.settings.lessons_url(self.semester)))
        # first sort by lesson name, then sort by teacher name
        lessons = [[x["wlkcid"], utils.escape_str(x["kcm"]), x["jsm"], x["kch"]]
                   for x in content["resultList"] if (x["kcm"] not in exclude) and (include == [] or x["kcm"] in include or utils.escape_str(x["kcm"]) in include)]

        lessons.sort(key=lambda x: (x[1], x[2]))

        # create a helper function to determine the folder name
        for i in range(len(lessons)):
            _, kcm, jsm, kch = lessons[i]

            # check the previous and next lesson to
            # determine the naming method of the current lesson
            prev_lesson = lessons[i-1] if i-1 >= 0 else None
            next_lesson = lessons[i+1] if i+1 < len(lessons) else None

            if (prev_lesson is None or prev_lesson[1] != kcm) and \
               (next_lesson is None or next_lesson[1] != kcm):
                lessons[i].append(kcm)
            elif (prev_lesson is None or prev_lesson[1] != kcm or
               prev_lesson[2] != jsm) and \
               (next_lesson is None or next_lesson[1] != kcm or
               next_lesson[2] != jsm):
                lessons[i].append(f"{kcm}_{jsm}")
            else:
                lessons[i].append(f"{kcm}_{kch}")
        return lessons

    def init_lessons(self, exclude, include):
        """Make directories for the lessons.
        
        This method creates directories for the lessons based on the list of lessons returned by `get_lessons()`. The directories are created in the specified path set by `set_path()`. If the directories already exist, they are not created again.
        
        Args:
            exclude (list):         `exclude` parameter for `get_lessons()`. List of lesson names to exclude.
            include (list):         `include` parameter for `get_lessons()`. List of lesson names to include. If specified, only lessons with names in this list will be included.

        Returns:
            lessons (list):         The return from `get_lessons()`. List of lessons, each represented as a list of the form [_lesson_id_, _lesson_name_, _teacher_name_, _course_code_, _folder_name_].
        """
        lessons = self.get_lessons(exclude=exclude, include=include)

        for i in range(len(lessons)):
            self.fm.mkdirl(os.path.join(self.path, lessons[i][4]))
        return lessons

    def get_files_id(self, lesson_id):
        """Get the list of file IDs for a lesson.

        This method sends a request to the platform to get the list of file IDs for a lesson. The list is then sorted by **file name** ("wjmc").

        Args:
            lesson_id (str):        ID of the lesson to get files for.

        Returns:
            files_id (list):        List of file IDs.
        """
        form = {"wlkcid": lesson_id}
        files = self.jh.loads(self._get(self.settings.files_url, params=form))
        files_id = [row["id"] for row in files["object"]["rows"]] if files["object"] else []

        return files_id

    def file_id_exist(self, fid):
        """Check if a file ID exists in the local file."""
        return (fid in self.local)

    def save_file_id(self, fid, fpath):
        """Save the file ID to the local file."""
        if (fid not in self.local):
            self.local.add(fid)
            self.fm.append(self.settings.local_file_path, fid+" "+fpath)

    def download_files(self, lesson_id, lesson_name, file_id):
        """Download files for a lesson.
        
        This method uses the file ID to download the files for a lesson. The files are saved in the specified path set by `set_path()`. If the files already exist, they are not downloaded again.
        
        Args:
            lesson_id (str):        ID of the lesson to download files for.
            lesson_name (str):      Name of the lesson.
            file_id (str):          ID of the file to download.
        """
        # file_id example "sjqy_26ef84e7689589e90168990b993830641"
        files = self.jh.loads(self._get(self.settings.file_url(lesson_id, file_id)))
        for f in files["object"]:
            # fid example "2007990011_KJ_1548755901_04ee49a1-
            # 3a86-4b4e-841a-b5b55e789234_sjqy01-admin"
            fid = f[7]
            if (not self.file_id_exist(fid)):
                self._get(self.settings.download_before_url(fid))
                fs = self.session.get(self.settings.download_url(fid), stream=True)
                if 'Content-Disposition' in fs.headers:
                    fname, extension = os.path.splitext(
                        fs.headers["Content-Disposition"][22:-1])
                elif 'ETag' in fs.headers:
                    fname, extension = os.path.splitext(fs.headers['ETag'])
                else:
                    print('not found name')
                    exit(0)
                # fix special character that exists in filename
                real_filename = utils.escape_str(f[1])
                fpath = os.path.join(self.path, lesson_name, "file",
                                     real_filename + extension)
                self.fm.downloadto(fpath, fs, real_filename + extension)
                self.save_file_id(fid, fpath)

    def download_homework(self, lesson_id, lesson_name, download_submission, download_files=True):
        """Download homework for a lesson.
        
        This method uses the lesson ID to download the homework for a lesson. The homework is saved in the specified path set by `set_path()`. If the homework already exists, it is not downloaded again.
        
        Args:
            lesson_id (str):                ID of the lesson to download homework for.
            lesson_name (str):              Name of the lesson.
            download_submission (bool):     Whether to download the submissed homework.
            download_files (bool):          Whether to download the files.
            
        Returns:
            ddls (list):    List of homework deadlines, each represented as a list of the form [_lesson_name_, _homework_title_, _deadline_, _size_, _readme_].
        """
        ddls = []
        if download_files:
            try:
                with open(self.settings.user_file_path, "r") as f:
                    lines = f.readlines()
                    port = lines[2].replace('\n', '').replace('\r', '')
                if self.reset:
                    print("The port in config file is:", port)
                    port = input("Input the port (press Enter to skip): ")
                # assert port as an integer
                assert port.isdigit()
                self.settings.port = port
            except Exception as e:
                if sys.stdout is not None and sys.stdout.isatty() and self.reset:
                    print(f"Warning: Failed to get the port, due to {e}")
                    port = input("Please input the port of the server: ")
                    self.settings.port = port
                    if port != "":
                        with open(self.settings.user_file_path, "a") as f:
                            f.write(f"{port}\n")
                else:
                    download_files = False

        for api in self.settings.homeworks_url(lesson_id):
            for hw in self.jh.loads(self._get(api))["object"]["aaData"]:
                content = self._get(self.settings.homework_url(lesson_id, hw))
                hw_title, hw_readme = self.soup.parse_homework(content, hw)
                print(f"  Fetched homework: {hw_title}")
                ddls.append([lesson_name, 
                             hw_title, 
                             hw["jzsjStr"], 
                             hw["wjmc"] + "   " + utils.size_format(int(hw["wjdx"])) if hw["wjmc"] is not None \
                                 else hw["zynrStr"] if hw["zynrStr"] != "" \
                                 else hw["zt"],
                             hw_readme
                             ])

                if download_files:
                    hw_dir = os.path.join(self.path, lesson_name, "homework",
                                        utils.escape_str(hw_title))
                    self.fm.init_homework(hw, hw_dir, hw_title, hw_readme)

                    # download annexes and images
                    annex_attrs, img_urls = self.soup.parse_annex(content)
                    for i, attr in enumerate(annex_attrs):
                        if i == 2 and not download_submission:
                            break
                        annex_name, download_url, annex_id = attr
                        annex_prefix = "answer_" if i == 1 else "reviewed_" if i == 3 else ""
                        if (annex_name != "NONE" and
                                not self.file_id_exist(annex_id)):
                            annex = self.session.get(download_url, stream=True)
                            fpath = os.path.join(hw_dir, annex_prefix+annex_name)
                            try:
                                self.fm.downloadto(fpath, annex, annex_name)
                                self.save_file_id(annex_id, fpath)
                            except Exception as e:
                                print(f"    Failed to download annex: {e}")
                            try:
                                # file path relative to the `self.path` directory
                                file_path = os.path.relpath(fpath, self.path)
                                # process the path for the server to handle "\", " ", Chinese characters, etc.
                                file_path = file_path.replace("\\", "/")
                                file_path = quote(file_path, safe=":/")
                                # add annexes to readme in `ddls` (ddls[-1][4])
                                ddls[-1][4] += f"\n[Assignment annex](https://localhost:{port}/{file_path})"
                            except Exception as e:
                                print(f"    Failed to add annex to README.md: {e}")
                            print(f"    Downloaded annexes.")
                    ddls[-1][4] += " (￣ェ￣;)"

                    # img_names = []
                    # for i, img_url in enumerate(img_urls):
                    #     img = self.session.get(img_url, stream=True)
                    #     img_name = f'''{i+1}_{img.headers.get(
                    #         'content-disposition').split(
                    #         'filename=')[1].strip('"')}'''
                    #     if img.content[:8] == b'\x89PNG\x0d\x0a\x1a\x0a':
                    #         img_name = os.path.splitext(img_name)[0] + ".png"
                    #     fpath = os.path.join(hw_dir, img_name)
                    #     self.fm.downloadto(fpath, img, img_name, quiet=True)
                    #     img_names.append(img_name)

                    # # add images to README.md
                    # if img_names:
                    #     readme_path = os.path.join(hw_dir, "README.md")
                    #     with open(readme_path, "r") as f:
                    #         content = f.readlines()
                    #     for i, line in enumerate(content):
                    #         if line.strip() in ["#### Description", "#### 作业说明"]:
                    #             insert_index = i + 1
                    #             break
                    #     for img_name in reversed(img_names):
                    #         content.insert(insert_index, f"![]({img_name})\n")
                    #     with open(readme_path, "w") as file:
                    #         file.writelines(content)
                print(f"    Downloaded files for {hw_title}.")
        return ddls

    def upload(self, homework_id, file_path, message):
        """Upload a file for a homework assignment.
        
        This method uploads a file for a homework assignment. The file is uploaded to the platform using the specified homework ID. The message is included in the form data for the upload request.
        
        Args:
            homework_id (str):      ID of the homework assignment.
            file_path (str):        Path to the file to upload.
            message (str):          Message to include with the upload.
        """
        form = self.settings.upload_form(homework_id, file_path, message)
        response = self.jh.loads(self._post(self.settings.upload_api, form=form,
                                 headers=self.settings.upload_headers))
        if response["result"] == "success":
            print("done")
        else:
            print(f"Error: assignment may have expired. Details:\n{response}")

    def get_ddl(self, lessons, download_submission=False, download_files=True):
        """Get the list of homework deadlines for the lessons.

        This method gets the list of homework deadlines for the lessons. The list is then sorted by **deadline**. If the homework has expired, it is not included in the list.

        Args:
            lessons (list):             List of lessons, each represented as a list of the form 
                                        [_lesson_id_, _lesson_name_, _teacher_name_, _course_code_, _folder_name_].
            download_submission (bool): Whether to download the submission.

        Returns:
            ddls (list):    List of homework deadlines, each represented as a list of the form [_lesson_name_, _homework_title_, _deadline_, _time_left_, _size_].
        """
        ddls = []
        for i, lesson in enumerate(lessons):
            print(f"Fetching homework for {lesson[1]} ({i+1}/{len(lessons)})...")
            ddls += self.download_homework(
                lesson[0], lesson[4], download_submission, download_files)
        # delete expired homework by comparing ddl[2] with current time
        ddls = [ddl for ddl in ddls if not utils.expired(ddl[2])]
        ddls.sort(key=lambda x: x[2])
        if len(ddls[0]) == 4:
            return [[ddl[0], ddl[1], ddl[2], utils.time_delta(ddl[2]), ddl[3]]
                    for ddl in ddls]
        else:
            return [[ddl[0], ddl[1], ddl[2], utils.time_delta(ddl[2]), ddl[3], ddl[4]]
                    for ddl in ddls]


def main():
    pass


if __name__ == "__main__":
    main()
