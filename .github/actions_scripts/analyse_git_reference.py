#!/usr/bin/python3

#
# on a triggered github workflow, this file does the decisions and variagles like
#   - shall the build be released (otherwise just run builds to check if there are errors)
#   - is it a prerelease
#   - title, tag etc of release_tag
#
# see the last lines of the file to see what variables are set
#


import sys
import os
import subprocess

# get the jamulus version from the .pro file
def get_jamulus_version(repo_path_on_disk):
    jamulus_version = ""
    with open (repo_path_on_disk + '/Jamulus.pro','r') as f:
        pro_content = f.read()
    pro_content = pro_content.replace('\r','')
    pro_lines = pro_content.split('\n')
    for line in pro_lines:
        line = line.strip()
        VERSION_LINE_STARTSWITH = 'VERSION = '
        if line.startswith(VERSION_LINE_STARTSWITH):
            jamulus_version = line[len(VERSION_LINE_STARTSWITH):]
            return jamulus_version
    return "UNKNOWN_VERSION"

def get_git_hash():
    return subprocess.check_output(['git', 'describe', '--match=xxxxxxxxxxxxxxxxxxxx', '--always', '--abbrev', '--dirty']).decode('ascii').strip()
    #return subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    #return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

if len(sys.argv) == 1:
   pass
else:
    print('wrong number of arguments')
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    raise Exception("wrong agruments")
    
    
print("")
print("GITHUB_REF is {}".format(os.environ.get('GITHUB_REF',"")))
print("GITHUB_HEAD_REF is {}".format(os.environ.get('GITHUB_HEAD_REF',"")))
print("GITHUB_BASE_REF is {}".format(os.environ.get('GITHUB_BASE_REF',"")))
print("GITHUB_WORKSPACE is {}".format(os.environ.get('GITHUB_WORKSPACE',"")))
print("GITHUB_REPOSITORY is {}".format(os.environ.get('GITHUB_REPOSITORY',"")))
print("")
    
    
# derive workspace-path
repo_path_on_disk = os.environ['GITHUB_WORKSPACE'] 

# derive git related variables
version_from_changelog = get_jamulus_version(repo_path_on_disk)
if "dev" in version_from_changelog:
    release_version_name = "{}-{}".format(version_from_changelog, get_git_hash())
    print("building an intermediate version: ", release_version_name)
else:
    release_version_name = version_from_changelog
    print("building a release version: ", release_version_name)


fullref=os.environ['GITHUB_REF']
reflist = fullref.split("/", 2)
pushed_name = reflist[2]


# run Changelog-script
os.system('perl "{}"/.github/actions_scripts/getChangelog.pl "{}"/ChangeLog "{}" > "{}"/autoLatestChangelog.md'.format(
    os.environ['GITHUB_WORKSPACE'],
    os.environ['GITHUB_WORKSPACE'],
    version_from_changelog,
    os.environ['GITHUB_WORKSPACE']
))

#release types: [ publish_to_release, is_prerelease ]
RELEASE_TYPE_NONE       = [ False, True ]
RELEASE_TYPE_RELEASE    = [ True, False ]
RELEASE_TYPE_PRERELEASE = [ True, True ]

# decisions about release, prerelease, title and tag
release_type = RELEASE_TYPE_NONE
is_prerelease = True

if fullref.startswith("refs/tags/"):
    print('this reference is a Tag')
    release_tag = pushed_name # tag already exists
    release_title="Release {}".format(release_version_name)
    
    if pushed_name.startswith("r"):
        if "beta" in pushed_name:
            print('this reference is a Beta-Release-Tag')
            release_type = RELEASE_TYPE_RELEASE
        else:
            print('this reference is a Release-Tag')
            release_type = RELEASE_TYPE_PRERELEASE
    else:
        print('this reference is a Non-Release-Tag')
        release_type = RELEASE_TYPE_NONE
elif fullref.startswith("refs/heads/"):
    print('this reference is a Head/Branch')
    release_type = RELEASE_TYPE_NONE
    release_title='Pre-Release of "{}"'.format(pushed_name)
    release_tag = "releasetag/"+pushed_name #better not use pure pushed name, creates a tag with the name of the branch, leads to ambiguous references => can not push to this branch easily
else:
    print('unknown git-reference type: ' + fullref)
    release_type = RELEASE_TYPE_NONE
    release_title='Pre-Release of "{}"'.format(pushed_name)
    release_tag = "releasetag/"+pushed_name #avoid ambiguity in references in all cases

#if codeql is only wanted on main repo, use next line
# if(GITHUB_REPOSITORY=="jamulussoftware/jamulus"):

if(fullref=="refs/heads/master"):
    print("master-commit")
    do_codeql = True
elif(os.environ.get('GITHUB_BASE_REF',"")=="refs/heads/master"):
    print("master-pull-request")
    do_codeql = True
else:
    print("no codeql necessary")
    do_codeql = False


publish_to_release = release_type[0]
is_prerelease      = release_type[1]

#helper function: set github variable and print it to console
def set_github_variable(varname, varval):
    if isinstance(varval, str):
        pass
    elif isinstance(varval, bool):
        varval=str(varval).lower()
    else:
        print("TODO: conversion for type {}".format(type(varval)))
        
    print("{}='{}'".format(varname, varval)) #console output
    print("::set-output name={}::{}".format(varname, varval))

print("")
#set github-available variables
set_github_variable("PUBLISH_TO_RELEASE", publish_to_release)
set_github_variable("IS_PRERELEASE", is_prerelease)
set_github_variable("RELEASE_TITLE", release_title)
set_github_variable("RELEASE_TAG", release_tag) 
set_github_variable("PUSHED_NAME", pushed_name)
set_github_variable("JAMULUS_VERSION", release_version_name)
set_github_variable("RELEASE_VERSION_NAME", release_version_name)
set_github_variable("DO_CODEQL", do_codeql)
