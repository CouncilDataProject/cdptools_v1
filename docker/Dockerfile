FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    software-properties-common

RUN add-apt-repository universe

RUN apt-get update && apt-get install -y \
    git \
    curl \
    ffmpeg \
    python3.6 \
    python3-pip

RUN pip3 install \
    git+https://github.com/CouncilDataProject/cdptools.git

WORKDIR /home/
