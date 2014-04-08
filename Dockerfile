FROM ubuntu:latest
MAINTAINER "Brian Harrington" <brian.harrington@coreos.com>

ENV DEBIAN_FRONTEND noninteractive
ENV INITRD no

RUN apt-get update
RUN apt-get -y install libmemcached-tools python-memcache

RUN mkdir /tmp/memcache

ADD dump /bin/
ADD load /bin/
ADD sample /bin/
ADD meminsert.py /bin/

CMD ["/bin/dump"]
