import os
import subprocess

def shell(cmd):
    os.system(cmd)
    return None

def shellRead(cmd):
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return (out, err)