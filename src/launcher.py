import os
import json
import subprocess

config_path = os.path.join(os.getcwd(), 'config.json')
configured = False

if os.path.exists(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        configured = 'config_path' in config and config['config_path']
    except Exception:
        configured = False

if configured:
    # 启动无控制台版本
    subprocess.Popen(['./without_console.exe'], shell=True)
else:
    # 启动带控制台版本
    subprocess.Popen(['./with_console.exe'], shell=True)