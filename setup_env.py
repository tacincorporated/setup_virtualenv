from __future__ import print_function
import shutil
import errno
import sys
import os.path as path
from subprocess import Popen, PIPE


VirtualEnvPATH = path.join(path.dirname(path.realpath(__file__)), "python_bin")

Virtualenv = 'virtualenv'

ModulesString = "requests==2.13.0 arrow==0.10.0"

Modules = ModulesString.split()


def run_cmd(*args):
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if p.returncode:
        error_message = "Command '{0}' had a problem. Output: {1}. Error: {2}".format(args, out, err)
        raise EnvironmentError(error_message)
    return out


def run_virtualenv(*args):
    run_cmd(Virtualenv, *args)


def have_virtualenv():
    run_virtualenv("-h")


def make_virtualenv():
    run_cmd(Virtualenv, VirtualEnvPATH)


def is_windows():
    return hasattr(sys, 'getwindowsversion')


def script_path(script):
    if is_windows():
        folder = "Scripts"
    else:
        folder = "bin"
    return path.join(VirtualEnvPATH, folder, script)


def install(module):
    run_cmd(script_path("pip"), "install", module)


def clean():
    try:
        shutil.rmtree(VirtualEnvPATH)
    except OSError as exception:
        if exception.errno != errno.ENOENT:
            raise

if __name__ == "__main__":
    clean()
    have_virtualenv()
    make_virtualenv()
    map(install, Modules)
    print("Your python virtualenv python is location at {0}.".format(script_path("python")))