FROM ubuntu:focal
RUN echo hallo von kaje
RUN echo halloa von kaj
RUN apt-get update 
RUN apt-get -y install sudo
#ENV DEBIAN_FRONTEND="noninteractive" 
#ENV TZ=Europe/London
#RUN apt-get -y install tzdata
COPY autobuild_apk_1_prepare.sh /autobuild_apk_1_prepare.sh
COPY autobuild_apk_2_build.sh /autobuild_apk_2_build.sh
COPY autobuild_apk_3_copy_files.sh /autobuild_apk_3_copy_files.sh
COPY install-qt.sh /install-qt.sh
RUN /bin/bash ./autobuild_apk_1_prepare.sh
RUN echo halloa von kaje
#ENTRYPOINT /bin/bash /build_qt_project.sh