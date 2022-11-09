FROM tensorflow/tensorflow:2.10.0-gpu

COPY . /project
WORKDIR /project/
RUN cd /project/
RUN pip install --upgrade pip setuptools wheel
RUN python -m pip install .
