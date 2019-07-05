FROM arm32v7/debian:stretch
LABEL maintainer="Steve Verhagen<scverhagen@gmail.com>"

#COPY qemu-arm-static /usr/bin

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip nginx  && rm -rf /var/lib/apt/lists/*
RUN pip3 install uwsgi
COPY ./nginx.conf /etc/nginx/sites-enabled/default

COPY ./ ./solarpi
WORKDIR ./solarpi
RUN pip3 install -r ./requirements.txt

ENV IN_DOCKER Yes
#ENV GPIO_PIN_FACTORY pigpio
#ENV PIGPIO_ADDR host.docker.internal

EXPOSE 80
CMD ./dockerscript.sh
