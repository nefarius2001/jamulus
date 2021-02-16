#FROM windows-latest ## does not work, github environment
#FROM mcr.microsoft.com/windows:10.0.17763.1217-amd64 ## lacks python
FROM python:3.9.1-windowsservercore-1809

RUN echo hallo von kaje

COPY autobuild_apk_1_prepare.ps1 /autobuild_apk_1_prepare.ps1
COPY autobuild_apk_2_build.ps1 /autobuild_apk_2_build.ps1
COPY autobuild_apk_3_copy_files.ps1 /autobuild_apk_3_copy_files.ps1
COPY install-qt.ps1 /install-qt.ps1

RUN echo halloa von kaje

RUN dir

RUN powershell Set-ExecutionPolicy RemoteSigned 

RUN dpowershell ./autobuild_apk_1_prepare.ps1 -test c

RUN echo halloa von kaje

#ENTRYPOINT /bin/bash /build_qt_project.sh