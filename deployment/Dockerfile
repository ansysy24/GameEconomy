FROM python:3.8.0
ENV PYTHONUNBUFFERED 1
RUN export DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND noninteractive
RUN dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get install -y --fix-missing && apt-get update -y && apt-get update

RUN apt-get install -y python3-pip \
    python3-setuptools \
    rpl \
    tzdata \
    strace \
    lsof \
    build-essential \
    cmake \
    wget \
    openssh-server
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./ /code/
EXPOSE 8080
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
