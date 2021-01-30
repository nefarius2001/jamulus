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
echo "lss ..debug"
ls ${1}/android-build/build/outputs/apk/debug/
  
echo ""
echo ""
echo "move"
mv ${1}/android-build/build/outputs/apk/debug/android-build-debug.apk ${1}/deploy/jamulus_${jamulus_version_name}_android.apk
