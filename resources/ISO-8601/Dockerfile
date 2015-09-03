FROM hardbyte/python3
#FROM elyase/pyrun:3.4

ENV HOME_APP=/validador

WORKDIR ${HOME_APP}
ADD . ${HOME_APP}


RUN chmod u+x ISO-8601.py && \
    pip install -r requirements.txt && \
    ln -sf /proc/self/fd /dev/

CMD ["/datasets/dataset.csv"]

ENTRYPOINT ["python", "ISO-8601.py", "--dataset"]