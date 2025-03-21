from . import utils
import platform
import getpass
import os
import sys


class FileManager():
    def __init__(self, settings):
        self.settings = settings

    def _mkdir(self, name):
        if not os.path.exists(name):
            os.makedirs(name)

    def mkdirl(self, name):
        """Make directory for lessons.
        
        This method will create a directory for lessons with the specified name, and create subdirectories for files and homework.

        Args:
            name (str):     The name of the directory.
        """
        self._mkdir(name)
        self._mkdir(os.path.join(name, "file"))
        self._mkdir(os.path.join(name, "homework"))

    def set_user(self):
        username, password = self.get_user(reset=False)
        if username:
            print("Current username:", username)
            print("Input your username (Student ID): ('Enter' to skip change)")
        else:
            print("Input your username (Student ID): ")
        new_username = input()
        if new_username:
            username = new_username
        if password:
            print("Input your password: ('Enter' to skip change)")
        else:
            print("Input your password: ")
        new_password = getpass.getpass()
        if new_password:
            password = new_password
        # save info to the first 2 lines of user.txt, keep the rest
        try:
            with open(self.settings.user_file_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []
        lines = [username + '\n', password + '\n'] + lines[2:]
        with open(self.settings.user_file_path, 'w') as f:
            f.writelines(lines)
        return (username, password)

    def get_user(self, reset=True):
        try:
            f = open(self.settings.user_file_path, 'r')
            lines = f.readlines()
            username = lines[0].replace('\n', '').replace('\r', '')
            password = lines[1].replace('\n', '').replace('\r', '')
            f.close()
        except:
            username, password = self.set_user() if reset else (None, None)

        return (username, password)

    def set_local(self):
        sf = open(self.settings.local_file_path, 'w')
        sf.close()

    def get_local(self):
        local = set()
        try:
            f = open(self.settings.local_file_path, 'r')
            lines = f.readlines()
            for line in lines:
                local.add(line.split()[0])
            f.close()
        except:
            self.set_local()
        return local

    def set_path(self):
        path = self.get_path(reset=False)
        if path:
            print("Current path:", path)
            print("Input new saving path: ('Enter' to skip change)")
        else:
            print("Input saving path for this semester:")
        input_path = input()
        if input_path:
            path = input_path
        sf = open(self.settings.path_file_path, 'w')
        print(path, file=sf)
        sf.close()
        return path

    def get_path(self, reset=True):
        try:
            f = open(self.settings.path_file_path, 'r')
            path = f.readlines()[0].replace('\n', '').replace('\r', '')
            f.close()
        except:
            path = self.set_path() if reset else None
        return path

    def append(self, fname, content):
        try:
            f = open(fname, 'a')
            print(content, file=f)
            f.close()
        except:
            pass

    def init_homework(self, hw, hw_dir, hw_title, hw_readme):
        if (not os.path.exists(os.path.join(hw_dir, ".xszyid"))):
            print("  Homework " + hw_title)

        self._mkdir(hw_dir)

        # try:
        #     f = open(os.path.join(hw_dir, "README.md"), 'w', encoding='utf-8')
        #     f.write(hw_readme)
        #     f.close()
        # except:
        #     pass

        if (not os.path.exists(os.path.join(hw_dir, ".xszyid"))):
            with open(os.path.join(hw_dir, ".xszyid"), "w") as f:
                f.write(hw["xszyid"])

    def downloadto(self, save_path, file_page, file_name, quiet=False):
        total_size = 0
        try:
            total_size = int(file_page.headers['Content-Length'])
        except:
            pass
        temp_size = 0
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w') if quiet else original_stdout
        print("  Fetch " + file_name + ".")
        if (not os.path.exists(save_path)):
            print("    Create " + file_name + "!")
        else:
            print("    Cover " + file_name + "!")
            if os.path.exists(save_path+".tmp"):
                os.remove(save_path+".tmp")
            os.rename(save_path, save_path+".tmp")
        try:
            with open(save_path, "wb") as local:
                for chunk in file_page.iter_content(chunk_size=1024 * 10):
                    if chunk:
                        temp_size += len(chunk)
                        sys.stdout.write(f"    Downloading file chunks to {utils.size_format(temp_size)}...".ljust(55) + "\r")
                        sys.stdout.flush()
                        local.write(chunk)
                        local.flush()
                        # if (total_size != 0):
                        #     done = int(30 * temp_size / total_size)
                        #     space = " "
                        #     if (platform.system() == "Windows"):
                        #         space = "  "
                        #     sys.stdout.write("\r[%s%s] %d%% %s/%s    \t" %
                        #                      ('█'*done, space*(30-done),
                        #                       100*temp_size / total_size,
                        #                       utils.size_format(temp_size),
                        #                       utils.size_format(total_size)))
                        #     sys.stdout.flush()
                        # else:
                        #     sys.stdout.write("\r\t%s/UNKNOWN    \t" %
                        #                      (utils.size_format(temp_size)))
                        #     sys.stdout.flush()
            # sys.stdout.write("\n")
        except KeyboardInterrupt:
            print("    Interrupted.".ljust(55) + "\n")
            if os.path.exists(save_path):
                os.remove(save_path)
            if os.path.exists(save_path+".tmp"):
                os.rename(save_path+".tmp", save_path)
        except Exception as e:
            sys.stdout.write(f"    Failed to download file: {e}\n")
            if os.path.exists(save_path):
                os.remove(save_path)
            if os.path.exists(save_path+".tmp"):
                os.rename(save_path+".tmp", save_path)
        if os.path.exists(save_path+".tmp"):
            os.remove(save_path+".tmp")
        sys.stdout.write("    Done.".ljust(55) + "\n")
        sys.stdout = original_stdout
