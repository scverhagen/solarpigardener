#FROM balenalib/raspberry-pi-debian:latest
FROM python:3.6-slim-stretch
LABEL maintainer="Steve Verhagen<scverhagen@gmail.com>"

RUN mkdir -p /etc/gardener

#build date/time (unix format)
RUN date > /build_date.txt

#RUN mkdir /etc/redis
#COPY ./redis.conf /etc/redis
#RUN apt-get update && apt-get install -o Dpkg::Options::="--force-confold" --force-yes -y redis-server python3 python3-dev python3-setuptools python3-pip build-essential && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -o Dpkg::Options::="--force-confold" --force-yes -y python3-setuptools build-essential apt-utils && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip

ENV IN_DOCKER Yes
EXPOSE 80

COPY ./ ./solarpi
WORKDIR ./solarpi
RUN pip3 install -r ./requirements.txt
CMD ./dockerscript.sh