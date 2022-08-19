FROM nginx:1.23

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && \
        apt-get -y dist-upgrade && \
        apt-get -y autoremove && \
        apt-get -y autoclean && \
        apt-get -y clean

COPY /target/etc/nginx/nginx.conf /etc/nginx/
