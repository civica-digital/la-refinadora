FROM hardbyte/python3
#FROM elyase/pyrun:3.4

ENV HOME_APP=/validador

WORKDIR ${HOME_APP}
ADD . ${HOME_APP}


RUN chmod u+x column-check.py && \
    ln -sf /proc/self/fd /dev/

CMD ["/datasets/dataset.csv"]

ENTRYPOINT ["python", "column-check.py", "--dataset"]
