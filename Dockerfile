# syntax=docker/dockerfile:1

FROM ubuntu:20.04

WORKDIR /kanop

COPY . .

RUN set -xe \
    && apt-get update \
    && apt-get -y install python3-pip
    
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0"]
