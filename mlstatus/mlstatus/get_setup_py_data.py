import os
import subprocess
import json

def get_setup_py_data(dirname):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    cmd='python '+dirpath+'/print_setup_py_data.py'
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirname)
    if result.stderr:
        print(result.stderr)
    if not result.stdout:
        return None
    obj=json.loads(result.stdout.decode())
    return obj