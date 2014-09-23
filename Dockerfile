FROM ubuntu:14.04
MAINTAINER Tomjo Soptame <tomjo.soptame@vokalinteractive.com>
RUN apt-get -qq update
RUN apt-get install -y socat git
RUN apt-get install -y python-pip python-dev python-psycopg2 libpq-dev  gunicorn
RUN apt-get install -y g++ make
RUN pip install virtualenv
RUN pip install -U fig
RUN apt-get install -y vim

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/
ADD fig.yml /code/
RUN cat requirements.txt
RUN pip install -r requirements.txt
ADD . /code/
WORKDIR /code/knowdaledge
