FROM arm32v7/debian:stretch-slim
LABEL maintainer="Steve Verhagen<scverhagen@gmail.com>"

#COPY qemu-arm-static /usr/bin

RUN apt update
RUN apt install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

COPY ./ ./solarpi
WORKDIR ./solarpi

RUN pip3 install -r requirements.txt

COPY ./nginx.conf /etc/nginx/sites-enabled/default

EXPOSE 80
CMD ./dockerscript.sh
