#!/bin/bash

# autobuild_2_build: actual build process


####################
###  PARAMETERS  ###
####################

source $(dirname $(readlink -f "${BASH_SOURCE[0]}"))/../ensure_THIS_JAMULUS_PROJECT_PATH.sh

###################
###  PROCEDURE  ###
###################

cd "${THIS_JAMULUS_PROJECT_PATH}"/distributions

if [ "${1}" = "headless" ]; then
  sh ./build-debian-package-auto.sh headless
else
  sh ./build-debian-package-auto.sh
fi
