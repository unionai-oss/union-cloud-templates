# 🐳📦 Docker containers unlock OS-level reproducibility 🔄
# docker build -t localhost:30000/onboarding:v0.1 .
# localhost:30000 is the registry that comes with flytectl demo start, you'll have to push after building
FROM python:3.9-slim-buster

WORKDIR /root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV GIT_PYTHON_REFRESH quiet

RUN apt-get update && apt-get install -y build-essential vim git
RUN pip3 install awscli

# Install Python dependencies
COPY ./requirements.txt /root
RUN pip install -r /root/requirements.txt

# Copy the actual code
COPY . /root
RUN pip install -e /root
