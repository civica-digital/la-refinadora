FROM alpine:latest
MAINTAINER "Miguel Angel Gordian"

RUN apk add --update build-base python3 python3-dev

WORKDIR /validadora
ADD . /validadora

RUN pip3 install -r requirements.txt && python3 setup.py install

RUN apk del build-base python-dev  && rm -rf /var/cache/apk/*

ENTRYPOINT python3 bin/run.py
