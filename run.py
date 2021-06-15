import subprocess
import os 
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))

# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
python_bin = dir_path + "/env/Scripts/python.exe"

# Path to the script that must run under the virtualenv
script_file = dir_path+"\graphics.py"

if not os.path.isdir(dir_path+"/env"):
    subprocess.check_call([sys.executable, "-m", "venv", "env"])
    subprocess.check_call([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_bin, "-m", "pip", "install","-r", "requirement.txt"])


subprocess.Popen([python_bin, script_file])