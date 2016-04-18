# mxabierto validadora
# Engine que corre una serie de validaciones sobre un dataset
# Build:
#   docker build -t mxabierto/validadora .
# Usage:
#   docker run --rm -it mxabierto/validadora

# Base image
FROM mxabierto/python3

MAINTAINER "Miguel Angel Gordian"

ADD . /validadora

WORKDIR /validadora

RUN \
  apk-install \
    build-base \
    python3-dev && \
  pip install -r requirements.txt && \
  python3 setup.py install && \
  apk del \
    build-base \
    python3-dev

ENTRYPOINT python3 bin/run.py
