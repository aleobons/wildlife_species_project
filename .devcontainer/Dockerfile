FROM tensorflow/tensorflow:2.9.1-gpu

ARG DEBIAN_FRONTEND=noninteractive

# Install apt dependencies
RUN apt-get update && apt-get install -y \
    git \
    gpg-agent \
    python3-cairocffi \
    protobuf-compiler \
    python3-pil \
    python3-lxml \
    python3-tk \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    sudo

# Install Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

RUN apt-get update
RUN apt-get -y install docker-ce

COPY ./requirements.txt requirements.txt
RUN pip3 -q install pip --upgrade
RUN pip install -r requirements.txt

ENV TF_CPP_MIN_LOG_LEVEL 3