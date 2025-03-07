import os
import sys
from pathlib import Path

from requests_toolbelt.multipart.encoder import MultipartEncoder

class Settings:
    def __init__(self, config_dir=None):
        self.headers = {
            'Connection': 'keep-alive', 
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*', 
            'User-Agent':   'Mozilla/5.0 (Linux; Android 6.0; '
                            'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/56.0.2924.87 Mobile Safari/537.36'
        }
        self.upload_headers = {
            'Connection': 'keep-alive', 
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*', 
            'User-Agent':   'Mozilla/5.0 (Linux; Android 6.0; '
                            'Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/56.0.2924.87 Mobile Safari/537.36',
            'Content-Type': 'multipart/form-data; '
                            'boundary=----WebKitFormBoundaryTytyPd5kgvE3t0kW'
        }

        if config_dir:
            self.config_dir = os.path.join(config_dir, ".config")
        else:
            if (os.name == 'nt'):
                self.config_dir = os.path.join(os.environ.get("APPDATA"), "WebLearningTHU", ".config")
            elif (os.name == 'posix'):
                self.config_dir = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "WebLearningTHU", ".config")
            else:
                self.config_dir = os.path.join(Path.home(), "WebLearningTHU", ".config")

        if (not os.path.exists(self.config_dir)):
            os.makedirs(self.config_dir)

        self.user_file_path = os.path.join(self.config_dir, "user.txt")
        self.local_file_path = os.path.join(self.config_dir, "local.txt")
        self.path_file_path = os.path.join(self.config_dir, "path.txt")
        self.port = None

        self.url = "https://learn.tsinghua.edu.cn/"
        self.login_id_url = "https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do"
        self.login_url = self.url + "b/j_spring_security_thauth_roaming_entry"
        self.semester_url = self.url + "b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester"
        self.semester_ref = self.url + "f/wlxt/index/course/student/"
        self.files_url = self.url + "b/wlxt/kj/wlkc_kjflb/student/pageList"
        self.upload_api = self.url + "b/wlxt/kczy/zy/student/tjzy"


    def file_url(self, lesson_id, file_id):
        return self.url+"b/wlxt/kj/wlkc_kjxxb/student/kjxxb/"+lesson_id+"/"+file_id


    def lessons_url(self, semester):
        return self.url+"b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/" + \
            "loadCourseBySemesterId/"+semester+"/en"


    def download_before_url(self, fid):
        return self.url+"b/kc/wj_wjb/downloadFileBefore?wjid="+fid


    def download_url(self, fid):
        return self.url+"b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid="+fid


    def homeworks_url(self, lesson_id):  # add "Ypg" if needed
        form = "aoData=[{\"name\":\"wlkcid\",\"value\":\""+lesson_id+"\"}]"
        types = ["Yjwg", "Wj", "Ypg"]
        return [self.url+"b/wlxt/kczy/zy/student/zyList"+x+"?"+form for x in types]


    def homework_url(self, lesson_id, hw):
        return self.url+"f/wlxt/kczy/zy/student/viewTj?wlkcid="+lesson_id + \
            "&sfgq=0&zyid="+hw["zyid"]+"&xszyid="+hw["xszyid"]


    def upload_form(self, homework_id, file_path, message):
        if (file_path == ''):
            return MultipartEncoder(
                fields={
                    'xszyid': homework_id,
                    'isDeleted': '1',
                    'zynr': message
                },
                boundary='----WebKitFormBoundaryTytyPd5kgvE3t0kW'
            )
        else:
            return MultipartEncoder(
                fields={
                    'fileupload': (os.path.basename(file_path),
                                open(file_path, 'rb'),
                                'application/octet-stream'),
                    'xszyid': homework_id,
                    'isDeleted': '0',
                    'zynr': message
                },
                boundary='----WebKitFormBoundaryTytyPd5kgvE3t0kW'
            )
