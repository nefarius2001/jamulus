#!/bin/bash

# Please run this script with the first parameter being the root of the repo
if [ -z "${1}" ]; then
    echo "Please give the path to the repository root as second parameter to this script!"
    exit 1
fi
		
		
mkdir ${1}/deploy

echo ""
echo ""
echo ""
echo "lss top"
ls ${1}
echo ""
echo ""
echo ""
echo "lss distributions"
ls ${1}/distributions
echo ""
echo ""
echo ""
echo ""
echo "lss linuxnormal"
ls ${1}/autobuild/linux/normal
echo ""
echo ""
echo ""
echo ""

mv ${1}/distributions/jamulus-headless*_amd64.deb ${1}/deploy/jamulus_headless_${jamulus_version_name}_ubuntu_amd64.deb
mv ${1}/distributions/jamulus*_amd64.deb          ${1}/deploy/jamulus_${jamulus_version_name}_ubuntu_amd64.deb
mv ${1}/jamulus-headless*_amd64.deb ${1}/deploy/jamulus_headless_${jamulus_version_name}_ubuntu_amd64.deb
mv ${1}/jamulus*_amd64.deb          ${1}/deploy/jamulus_${jamulus_version_name}_ubuntu_amd64.deb
