#!/bin/sh -e

# Create deb files

# set armhf
#sudo dpkg --add-architecture armhf

if [ "${1}" = "headless" ]; then
  cp -r debian-headless ../debian
else
  cp -r debian-gui ../debian
fi

cd ..

# get the jamulus version from pro file
VERSION=$(cat Jamulus.pro | grep -oP 'VERSION = \K\w[^\s\\]*')

# patch changelog (with hack)

CHANGELOGCONTENT="$(perl .github/actions_scripts/getChangelog.pl ChangeLog ${VERSION})"
dch "${CHANGELOGCONTENT}" -v "${VERSION}"


echo "${VERSION} building..."

sed -i "s/é&%JAMVERSION%&è/${VERSION}/g" debian/control

debuild -b -us -uc
# create deploy folder

mkdir deploy

if [ "${1}" = "headless" ]; then
  mv ../jamulus-headless*_amd64.deb deploy/  # no quotes for wildcard
else
  mv ../jamulus*_amd64.deb deploy/  # no quotes for wildcard
fi
