#!/usr/bin/python3

import os
from pathlib import Path
from lib_jamulus_version import JamulusQtProjectFile, query_abort, default_jamulus_project_path

def git_cmd(cmd):
    print(cmd)
    os.system(cmd)

if os.name == 'nt':
    editor = "notepad.exe"
elif os.name == 'posix':
    editor = "gedit"
else:
    raise Exception("unexpected os.name")

jamulus_qt_projectfile = JamulusQtProjectFile()
version_before = jamulus_qt_projectfile.get_version()
path_qt_projectfile = jamulus_qt_projectfile.qt_projectfile_path
path_changelog = Path(default_jamulus_project_path(), "ChangeLog")

print("current version for reference: {}".format(version_before))
inputString = input('Enter version to create      : ')

release_versionstring = inputString
release_tag_name = "r_" + inputString.replace(".","_")
if "beta" in release_tag_name:
    version_after = version_before
    changelog_edit_msg1 = "edit changelog now, please change the current paragraph to {}".format(release_versionstring)
    changelog_edit_msg2 = "edit changelog now, please change the current paragraph to {} (reverts former edit)".format(version_after)
else:
    version_after = release_versionstring + "dev"
    changelog_edit_msg1 = "edit changelog now, please change the current paragraph to {}, and append the date (conform to former entries)".format(release_versionstring)
    changelog_edit_msg2 = "edit changelog now, please add a paragraph for {} (appended with \"dev\")".format(version_after)


print("         version before  : {}".format(version_before))
print("         tag-version     : {}".format(release_versionstring))
print("         tag-name        : {}".format(release_tag_name))
print("         version after   : {}".format(version_after))
query_abort("Check the strings above! Proceed? ", default=None)

print("chdir to project path")
os.chdir(default_jamulus_project_path())

print("")
print(changelog_edit_msg1)
query_abort("are you ready to edit the Changelog?")
ret_val = os.system("{:} {:}".format(editor, path_changelog))
print("set version in qt-project-file")
jamulus_qt_projectfile.set_version(release_versionstring)


query_abort("shall we proceed to create the tag?")


print("")
print("create commit")
git_cmd("git add \"./{:}\"".format(path_changelog.relative_to(os.getcwd())))
git_cmd("git add \"./{:}\"".format(path_qt_projectfile.relative_to(os.getcwd())))
git_cmd("git commit -m \"version changed to {:}\"".format(release_versionstring))
print("create release-tag")
git_cmd("git tag \"{:}\"".format(release_tag_name))


print("")
print(changelog_edit_msg2)
query_abort("are you ready to edit the Changelog?")
ret_val = os.system("{:} {:}".format(editor, path_changelog))
print("set version in qt-project-file")
jamulus_qt_projectfile.set_version(version_after)

print("")
print("create commit")
git_cmd("git add \"./{:}\"".format(path_changelog.relative_to(os.getcwd())))
git_cmd("git add \"./{:}\"".format(path_qt_projectfile.relative_to(os.getcwd())))
git_cmd("git commit -m \"version changed to {:}\"".format(release_versionstring))








print("")
print("double-check the created commits in a different terminal before pushing (e.g. with gitk)")
query_abort("proceed to push the commits & tag?")
#git push ${git_remote_name}
#git push ${git_remote_name} "${release_tag_name}"

print("done")


