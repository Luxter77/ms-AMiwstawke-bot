FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV PATH            ${PATH}:/root/miwstawke

ENV ISDOCKER        true
ENV CHRISTIANSERVER true

RUN apt -qqqq update
RUN apt -qqqq install python3 python3-pip ca-certificates > /dev/null

WORKDIR /root/miwstawke/

ADD miwstawke miwstawke

COPY requirements.txt pain.py ./
COPY miwstawke                miwstawke/
COPY miwstawke/secrets.py     miwstawke

RUN pip3 install -r requirements.txt > /dev/null

ENTRYPOINT ["pain.py"]
