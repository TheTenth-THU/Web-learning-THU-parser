import os

class Settings:
    def __init__(self, config_dir=None):
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

        self.auth_file_path = os.path.join(self.config_dir, "auth.txt")
        self.changed_file_path = os.path.join(self.config_dir, "changed.txt")

        self.color_choices = ['berry_red', 'red', 'orange', 'yellow', 'olive_green', 'lime_green', 'green', 'mint_green', 'teal', 'sky_blue', 'light_blue', 'blue', 'grape', 'violet', 'lavender', 'magenta', 'salmon', 'charcoal', 'grey', 'taupe']

    def get_auth(self):
        try:
            f = open(self.auth_file_path, 'r')
            lines = f.readlines()
            auth_key = lines[0].replace('\n', '').replace('\r', '')
            f.close()
        except:
            auth_key = None
        return auth_key

    def set_auth(self, auth_key):
        sf = open(self.auth_file_path, 'w')
        print(auth_key, file=sf)
        sf.close()
        return auth_key