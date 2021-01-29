#!/bin/bash

# Please run this script with the first parameter being the root of the repo
if [ -z "${1}" ]; then
    echo "Please give the path to the repository root as second parameter to this script!"
    exit 1
fi

cd ${1}
		
		
cd ${1}/distributions

sudo ./build-debian-package-auto.sh

mkdir ${1}/deploy

#debuild -b -us -uc -aarmhf
# copy for auto release
cp ${1}/../*.deb ${1}/deploy/

# rename them

mv ${1}/deploy/jamulus-headless*_amd64.deb ${1}/deploy/Jamulus_headless_amd64.deb
mv ${1}/deploy/jamulus*_amd64.deb ${1}/deploy/Jamulus_amd64.deb
