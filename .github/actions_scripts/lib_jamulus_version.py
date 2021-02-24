#!/usr/bin/python3

#library for detecting/manipulating the version strings

import sys
import subprocess
import os
from pathlib import Path

QT_PROJECTFILE_VERSION_LINE_STARTSWITH = 'VERSION = '

def default_jamulus_project_path():
    return Path(__file__).parent.parent.parent.absolute()


# a class to handle the versionstring in the .pro file
class JamulusQtProjectFile:
    def __init__(self, repo_path_on_disk=default_jamulus_project_path()):
        self.qt_projectfile_path=Path(repo_path_on_disk, 'Jamulus.pro')

    def get_version(self):
        with open (self.qt_projectfile_path,'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith(QT_PROJECTFILE_VERSION_LINE_STARTSWITH):
                    jamulus_version = line[len(QT_PROJECTFILE_VERSION_LINE_STARTSWITH):]
                    return jamulus_version
        return None

    def set_version(self, versionstring_to_set):
        QT_PROJECTFILE_VERSION_LINE_BEFORE = QT_PROJECTFILE_VERSION_LINE_STARTSWITH + self.get_version()
        QT_PROJECTFILE_VERSION_LINE_AFTER = QT_PROJECTFILE_VERSION_LINE_STARTSWITH + versionstring_to_set
        with open(self.qt_projectfile_path,'r') as f:
            pro_content = f.read()
        pro_content = pro_content.replace(QT_PROJECTFILE_VERSION_LINE_BEFORE, QT_PROJECTFILE_VERSION_LINE_AFTER)
        with open(self.qt_projectfile_path,'w') as f:
            f.write(pro_content)


# get the jamulus version from the .pro file
def get_jamulus_version(repo_path_on_disk=default_jamulus_project_path()):
    return JamulusQtProjectFile(repo_path_on_disk).get_version()

def get_git_hash():
    return subprocess.check_output(
        ['git', 'describe', '--match=xxxxxxxxxxxxxxxxxxxx', '--always', '--abbrev', '--dirty']).decode('ascii').strip()
    # return subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    # return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

# from https://code.activestate.com/recipes/577058/
def query_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " \
                             "(or 'y' or 'n').\n")


def query_abort(question, default=None):
    choice = query_yes_no(question=question, default=default)
    if choice != "yes":
        print("aborting");
        exit(0)


if __name__ == "__main__":
    print("developing/debugging this library")
    print("get_jamulus_version: {}".format(get_jamulus_version()))
    #print("get_jamulus_version: {}".format(JamulusQtProjectFile().get_version()))
    #JamulusQtProjectFile().set_version("TTT")
    #print("get_jamulus_version: {}".format(JamulusQtProjectFile().get_version()))
    release_prepare()
